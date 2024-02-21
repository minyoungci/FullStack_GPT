import streamlit as st 
from langchain.document_loaders import SitemapLoader


@st.cache_data(show_spinner="Loading Website...") # load_website가 한 번 실행된 후 , 같은 url로 다시 호출되면 아무 일도 하지 않도록 설정
def load_website(url):
    loader = SitemapLoader(url) 
    loader.headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
    loader.request_per_second = 5
    docs = loader.load()
    return docs 

st.set_page_config(
    page_title="SiteGPT",
    page_icon="🧊",
)

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
    if ".xml" not in url:
        with st.sidebar:
            st.error("Please write down a Sitemap URL.")
    else:
        docs = load_website(url)
        st.write(docs)