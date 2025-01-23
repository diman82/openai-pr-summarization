import tensorflow as tf
import tensorflow_hub as hub

from llm_engine.functions import check_streamlit_used


class TfHubUniversalSentenceEncoder:
    def __init__(self):
        module_url = 'https://tfhub.dev/google/universal-sentence-encoder/4'
        self.embed = hub.load(module_url)
        self.corr = None
        # tf.config.run_functions_eagerly(True)

    def calc_similarity(self, input_text1, input_text2):
        messages = [input_text1, input_text2]
        accuracy = []
        message_embeddings_ = self.embed(messages)

        self.corr = tf.experimental.numpy.inner(message_embeddings_, message_embeddings_)
        tensor_obj = self.corr[0, 1]
        numpy_res: float = tf.get_static_value(tensor_obj)  # get numpy value from tensor object
        accuracy.append(numpy_res)
        if check_streamlit_used:
            import streamlit as st
            st.session_state["similarity_score"] = "%.2f" % accuracy[0]
            return st.session_state["similarity_score"]
        else:
            return accuracy[0]
