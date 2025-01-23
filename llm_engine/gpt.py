import os
from typing import List

import openai
import logging
import sys

from llm_engine.functions import clear_and_return_res, check_streamlit_used

sys.path.append('.')

TEMPERATURE = .5
MAX_TOKENS = 500
CHATGPT_TOKEN_LIMIT = 8192  # current 'gpt-4' model limitation


class GPTEngine:
    """
    A wrapper class for making a direct call to ChatGPT llm_engine. An auxiliary logic has been
    implemented, to split large input text > than current CHATGPT_TOKEN_LIMIT (8192) into 'paragraphs', identified in
    by a simple '\n\n' rule, then passing each chunk through the llm_engine and finally combining all
    results and pushing it one last time through the llm_engine
    """
    @staticmethod
    def summarize(prefix: str, prompt: str, temperature=TEMPERATURE, max_tokens=MAX_TOKENS) -> str:
        openai.api_key = os.getenv('OPENAI_KEY')
        messages = [{"role": "user", "content": prefix+prompt}]
        try:
            res = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )["choices"][0]["message"]["content"]
            return clear_and_return_res(res)
        except Exception as e:
            if check_streamlit_used:
                import streamlit as st
                st.write('An error happened within "Summarize input text" function')
                st.exception(e)
            else:
                logging.exception('An error happened within "Summarize input text" function, exact message is:\n', e)

    # splitting large article ('gpt-4' model limit is 8192 tokens) into smaller chunks
    @staticmethod
    def summarize_large_article_by_paragraph_splitting(prompt, temperature=TEMPERATURE, max_tokens=MAX_TOKENS) -> str:
        # There is no lib/module that supports splitting by paragraphs, simply because there is no standard way to
        # agree what a paragraph is. Current implementation implies that a paragraph is separated by a double newline
        # character. splitting large article (> 4096 tokens) into smaller chunks TODO: add notification about
        #  splitting, print number of chunks/api calls
        if check_streamlit_used():
            import streamlit as st
            st.warning('Splitting large text to chunks', icon="⚠️")
        else:
            logging.warning('Splitting large text to chunks')
        chunks: List[str] = list(filter(lambda x: x != '', prompt.split('\n\n')))
        chunks_results: List[str] = list(map(lambda x: GPTEngine.summarize(x, temperature, max_tokens), chunks))
        new_prompt = '\n\n'.join(chunks_results)
        res = GPTEngine.summarize(new_prompt, temperature, max_tokens)  # last run through api to get summary of the all chunks
        return clear_and_return_res(res)
