from typing import List, Union
import tiktoken
from bs4 import BeautifulSoup, element


def summarize_large_article_by_embedding(prompt, temperature, max_tokens) -> List[str]:
    # TODO: split large article using 'text-embedding-ada-002' model into smaller chunks
    raise NotImplementedError


def _get_pr(pr_url: str) -> str:
    # TODO: fetch SA PR article directly from web OR from data platform
    raise NotImplementedError


def clear_text(text_box_objs: Union[List, str]):
    import streamlit as st
    if len(text_box_objs) == 0:
        raise ValueError("text_box_objs must be a non-empty string")
    elif len(text_box_objs) == 1:
        st.session_state[text_box_objs[0]] = ""
    else:
        for text_box_obj in text_box_objs:
            st.session_state[text_box_obj] = ""


def num_tokens_from_string(string: str, encoding_name: str = "gpt2") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def clear_and_return_res(result):
    # workaround for different usage for app and library
    if check_streamlit_used():
        import streamlit as st
        clear_text("summary")
        st.session_state["summary"] = result
        return st.session_state["summary"]
    else:
        return result


def check_streamlit_used() -> bool:
    """
    Function to check whether python code is run within streamlit or not
    Returns
    -------
    use_streamlit : boolean
        True if code is run within streamlit, else False
    """
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if not get_script_run_ctx():
            use_streamlit = False
        else:
            use_streamlit = True
    except ModuleNotFoundError:
        use_streamlit = False
    return use_streamlit


def get_tables_from_html(content: str, filter_criteria=None, table_delimiter="|") -> list:
    soup: BeautifulSoup = BeautifulSoup(content, 'lxml')
    tables: element.ResultSet = soup.find_all('table')
    list_tables: list = []
    for indx, table in enumerate(tables):
        if table.find('tbody'):
            table_body: element.Tag = table.find('tbody')
            rows: element.ResultSet = table_body.find_all('tr')
            data_comma: list = []
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data_comma.append([ele for ele in cols])  # Get rid of empty values
            data_pipe: list = [table_delimiter.join(x) for x in data_comma]
            table: str = "\n".join(data_pipe)
            list_tables.append(f"table {indx}: {table}")
    if list_tables:
        if filter_criteria:
            list_tables = [tbl for tbl in list_tables if
                           any(criteria.lower() in tbl.lower() for criteria in filter_criteria)]
        return list_tables
    return None
