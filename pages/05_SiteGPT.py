import streamlit as st 
from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import Html2TextTransformer # html

st.set_page_config(
    page_title="SiteGPT",
    page_icon="🧊",
)

html2text_transformer = Html2TextTransformer()

st.markdown(
    '''
    # Site GPT
    Ask questions about the content of a website.
    Start by writing the URL of the website on the sidebar
    '''
)

st.title("Site GPT")

# 웹 사이트의 모든 data, text를 스크랩해보자 
# 사이드바에서 URL을 입력받아서, 그 URL로부터 데이터를 받아오는 것을 구현해보자.

# 두 가지 방법이 있음.
# 1. playwright와 chromuium을 사용해서 웹사이트를 스크랩 (js코드가 많은 웹사이트의 경우 유용함. 셀레니움과 비슷, 웹 사이트가 모든 api로부터 data를 load할 때까지 조금 기다려야함.)

# 2. 직접 각 웹사이트의 sitemap을 추출

# 동적인 웹사이트는 1번 방법 , 정적인 사이트는 2번 방법 사용.

with st.sidebar:
    url = st.text_input("Write down a URL", placeholder="https://example.com",
                        )
    
if url:
    loader = AsyncChromiumLoader([url])
    docs = loader.load()
    transformed = html2text_transformer.transform_documents(docs) # html을 text로 변환
    st.write(docs)