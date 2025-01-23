import logging
import os
from llama_index.core import GPTVectorStoreIndex, Document

import nltk
# nltk.download('punkt')
import sys

from llm_engine.functions import clear_and_return_res, check_streamlit_used

sys.path.append('.')


class LlamaEngine:
    """
    The working paradigm that has emerged is in-context learning (the other is fine-tuning),
    where we insert context into the input prompt.
    That way, we take advantage of the LLM’s reasoning capabilities to generate a response.
    More info: https://gpt-index.readthedocs.io/en/latest/index.html
    ** We use it, to be able to feed input > than current CHATGPT_TOKEN_LIMIT (4096) **
    """

    @staticmethod
    def summarize(prefix: str, prompt: str, temperature=None, max_tokens=None) -> str:
        os.getenv('OPENAI_API_KEY')
        index = LlamaEngine._vectorize(prompt)  # call to Chat-GPT
        query_engine = index.as_query_engine()
        try:
            res = query_engine.query(prefix+prompt)
            return clear_and_return_res(res)
        except Exception as e:
            if check_streamlit_used:
                import streamlit as st
                st.write('An error happened within "Summarize" function')
                st.exception(e)
            else:
                logging.exception('An error happened within "Summarize input text" function, exact message is:\n', e)

    @staticmethod
    def _vectorize(input_doc: str):
        # Construct a simple vector index
        # input_list = nltk.word_tokenize(input_doc)
        # documents = [Document(text=t) for t in input_list]
        documents = [Document(text=input_doc)]
        return GPTVectorStoreIndex.from_documents(documents)
