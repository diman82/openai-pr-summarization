import streamlit as st

from authentication_engine.auth_engine_types import AuthEngine
from authentication_engine.basic_auth import BasicAuthentication
from authentication_engine.google_oauth import GoogleOauthAuthentication
from llm_engine.functions import num_tokens_from_string
from llm_engine.gpt import *
from llm_engine.engine_types import Engine
from llm_engine.llama import LlamaEngine
from llm_engine.similarity import TfHubUniversalSentenceEncoder


try:
    st.title("ChatGPT Text Summarizer")
    # initialize if None (otherwise yields an error)
    for session_item in ["input", "summary", "similarity_score", "name", "username", "authentication_status"]:
        if session_item not in st.session_state:
            st.session_state[session_item] = ""

    # Authentication
    if st.session_state["authentication_status"] == "":  # execute only if haven't been already authenticated
        st.subheader("Authentication")
        selected_auth_engine_type = st.selectbox("Authentication Engine Type", [engine.value for engine in AuthEngine])
        if selected_auth_engine_type == AuthEngine.OAUTH.value:
            token = st.text_input("Enter your Google ID token", type="password")
            auth_engine = GoogleOauthAuthentication()
            st.session_state["authentication_status"] = auth_engine.authenticate(token)
        else:
            auth_engine = BasicAuthentication()
            st.session_state["authentication_status"] = auth_engine.authenticate()

    # Content
    if st.session_state["authentication_status"] is True:
        st.success(f"Authentication successful with name: {st.session_state['name']}")

        # Continue with the rest of your app logic here
        openai.api_key = os.getenv('OPENAI_KEY')
        # bullet_points_switch = st.select_slider(label="Bullet points slider Toggle:", options=[True, False])
        bullet_points_switch = st.checkbox(label="Bullet points slider Toggle:", value=True,
                                           help='Toggle to enable bullet points')
        bullet_points_count = st.empty() if bullet_points_switch is False else st.slider("Number of bullet points",
                                                                                         min_value=1, max_value=10,
                                                                                         value=4)
        prefix_text = st.text_area(label='Prefix text before input text:',
                                   value='' if bullet_points_switch is False else f'You are a financial analyst. '
                                                                                  f'Summarize the following article '
                                                                                  f'in {bullet_points_count} bullet points. '
                                                                                  f'Ignore quotes:\n\n',
                                   height=68)
        input_text = st.text_area(label='Input text:', value=st.session_state['input'], height=250)
        token_count_textbox = st.empty()
        selected_engine = st.selectbox("Engine Type", [engine.value for engine in Engine])
        slider_temperature = st.slider("temperature", min_value=0.1, max_value=0.9, value=.3)
        slider_max_tokens = st.slider("max_output_tokens", min_value=50, max_value=1000, value=250)
        with st.spinner('Calculating token count..'):
            num_tokens = num_tokens_from_string(input_text)
        gpt_summarize_fn = GPTEngine.summarize \
            if num_tokens <= CHATGPT_TOKEN_LIMIT - MAX_TOKENS \
            else GPTEngine.summarize_large_article_by_paragraph_splitting
        selected_summarize_fn = gpt_summarize_fn \
            if selected_engine == Engine.GPT.value \
            else LlamaEngine.summarize if prefix_text != '' else st.error('Prefix can"t be empty for Llama '
                                                                          'llm_engine', icon="⚠️")
        with st.spinner('Generating summary..'):
            st.button("Generate summary",
                      help="Summarize input text",
                      on_click=selected_summarize_fn,
                      kwargs={"prefix": prefix_text, "prompt": input_text,
                              "temperature": slider_temperature, "max_tokens": slider_max_tokens})
        token_count_textbox.code(f"Token count: {num_tokens}")
        calc_similarity = st.empty()  # Appends an empty slot to the app. We'll use this later.
        output_text = st.text_area(label='Summarized text:', value=st.session_state['summary'], height=250)
        sentences_encoder_engine = TfHubUniversalSentenceEncoder()
        similarity_score = '!! one of the input text fields is empty !!'
        calculate_similarity_fn = st.write(f'Similarity score is: {similarity_score}') \
            if input_text == "" or output_text == "" else sentences_encoder_engine.calc_similarity
        with st.spinner('Calculating similarity..'):
            st.button("Calculate similarity",
                      help="Calculate similarity between input and output text",
                      on_click=calculate_similarity_fn,
                      kwargs={"input_text1": input_text, "input_text2": output_text})
        similarity_score_textbox = st.empty()
        similarity_score_textbox.code(f"Similarity score is: {st.session_state['similarity_score']}")
except Exception as e:
    st.write('There was an error =(')
    st.exception(e)
