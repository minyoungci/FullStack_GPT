from langchain.document_loaders import SitemapLoader
from langchain.document_transformers import Html2TextTransformer 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
import streamlit as st

def parse_page(soup):
    header = soup.find("header")
    footer = soup.find("footer")
    if header:
        header.decompose()
    if footer:
        footer.decompose()
    return (
        str(soup.get_text())
        .replace("\n", " ")
        .replace("\xa0", " ")
        .replace("CloseSearch Submit Blog", "")
    )

@st.cache_data
def load_website(url):
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=800,
        chunk_overlap=200,
    )
    loader = SitemapLoader(
        url,
        filter_urls=[
            r"^(.*\/blog\/).*",
        ],
        parsing_function=parse_page,
    )
    docs = loader.load_and_split(text_splitter=splitter)
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