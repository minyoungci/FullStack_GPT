import json
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser

import streamlit as st
from datetime import datetime

start_time = datetime.now()
print(
    f"\n\033[43mSTART Exec: {start_time.strftime('%H:%M:%S.%f')} =========================================\033[0m"
)

st.set_page_config(
    page_title="QuizGPT | D26 과제",
    page_icon="☘️",
)

st.title("D26 | QuizGPT Turbo")
with st.expander("과제 내용 보기", expanded=False):
    # st.snow()
    st.markdown(
    """
        Cloudflare 공식문서를 위한 SiteGPT 버전을 만드세요.
        챗봇은 아래 프로덕트의 문서에 대한 질문에 답변할 수 있어야 합니다:
        AI Gateway
        Cloudflare Vectorize
        Workers AI
        사이트맵을 사용하여 각 제품에 대한 공식문서를 찾아보세요.
        여러분이 제출한 내용은 다음 질문으로 테스트됩니다:
        "llama-2-7b-chat-fp16 모델의 1M 입력 토큰당 가격은 얼마인가요?"
        "Cloudflare의 AI 게이트웨이로 무엇을 할 수 있나요?"
        "벡터라이즈에서 단일 계정은 몇 개의 인덱스를 가질 수 있나요?"
        유저가 자체 OpenAI API 키를 사용하도록 허용하고, st.sidebar 내부의 st.input에서 이를 로드합니다.
        st.sidebar를 사용하여 Streamlit app과 함께 깃허브 리포지토리에 링크를 넣습니다.
    """
    )

with st.sidebar:
    if "api_key" not in st.session_state:
        st.session_state["api_key"] = ""

    api_key_input = st.empty()

    def reset_api_key():
        st.session_state["api_key"] = ""
        print(st.session_state["api_key"])

    if st.button(":red[Reset API_KEY]"):
        reset_api_key()

    api_key = api_key_input.text_input(
        ":blue[OpenAI API_KEY]",
        value=st.session_state["api_key"],
        key="api_key_input",
    )

    if api_key != st.session_state["api_key"]:
        st.session_state["api_key"] = api_key
        st.rerun()

    # print(api_key)

    st.divider()
    st.markdown(
        """
        GitHub 링크: https://github.com/minyoungci/FullStack_GPT/blob/master/recap/QuizGPT.py
        """
    )
