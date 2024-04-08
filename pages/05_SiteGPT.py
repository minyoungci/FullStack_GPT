from langchain.document_loaders import SitemapLoader
from langchain.document_transformers import Html2TextTransformer 
from langchain.chat_models import ChatOpenAI
import streamlit as st

@st.cache_data
def load_website(url):
    loader = SitemapLoader(url)
    docs = loader.load()
    st.write(docs)
    return docs


st.set_page_config(
    page_title="QuizGPT | D26 과제",
    page_icon="☘️",
)

st.markdown(
    """
    Welcome to SiteGPT
    """
)

html2text_transformer = Html2TextTransformer()  


llm = ChatOpenAI(
    temperature=0.1,
)


with st.sidebar: 
    url = st.text_input(
        "Write down a URL", 
        placeholder="https://example.com",
        )

if url :
    if ".xml" not in url:
        with st.sidebar:
            st.error("Please enter a valid URL")    

    else:
        docs = load_website(url)