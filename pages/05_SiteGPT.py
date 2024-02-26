import streamlit as st 
from langchain.document_loaders import SitemapLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 수정
def parse_page(soup): # 우리가 포함하고 싶은 text를 반환하는 함수. document의 전체 HTML을 가진 beautiful soup object 값이 여기에 오게 됨.즉 여기서 검색 가능
    header = soup.find("header") # 섹션을 선택할 수 있음. header,data,footer 등등
    footer = soup.find("footer")
    if header:
        header.decompose() # decompose()는 tag와 content를 분리해서 제거

    if footer:
        footer.decompose()
 # print("hello")시 사이트에서 가져온 값들을 보면 Hello가 프린트되어 있는데, 이는 parse_page function이 stiemap의 모든 URL에 대해 실행되었음을 의미함.
 # header에 있는 text를 반환하는 것을 확인할 수 있음.
    return (
        str(soup.get_text())  # get_text()는 모든 text를 반환함. 전체 페이지에서 header footer를 제거한 나머지 텍스트 반환
        .replace("\n", " ") # 필요없는 부분들을 replace로 제거(header, footer, 공백 문자, 필요없는 각종 버튼 제거)
        .replace("\xa0", " ")
        .replace("CloseSearch Submit Blog", " ")    
    )


@st.cache_data(show_spinner="Loading Website...") # load_website가 한 번 실행된 후 , 같은 url로 다시 호출되면 아무 일도 하지 않도록 설정
def load_website(url):
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=800,
    chunk_overlap=200,
    )

    loader = SitemapLoader(                  # URL 필터  
        url,
        filter_urls=[
            r"^(.*\/careers\/).", # data를 load 하고싶은 url들을 담은 list 
        ],
        parsing_function = parse_page         
    ) 
    loader.headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
    loader.request_per_second = 5
    docs = loader.load_and_split(text_splitter=splitter) # load_and_split은 모든 URL을 load하고, parsing_function을 적용한 후, text_splitter를 적용하여 text를 나누는 것을 의미함.
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