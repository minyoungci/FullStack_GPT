import streamlit as st 
import time


st.set_page_config(
    page_title = 'DocumentGPT',
    page_icon='🧊',
)

st.title("DocumentGPT")

if "messages" not in st.session_state: # messages가 session_state에 없는지 확인
    st.session_state["messages"] = [] # 없으면 intialize 해준다.


def send_message(message, role, save=True):
    with st.chat_message(role):
        st.write(message)
    if save:
        st.session_state["messages"].append({"message": message, "role": role}) # session_state는 리스트에 저장이 된다 ! 


for message in st.session_state["messages"]:
    send_message(
        message["message"],
        message["role"],
        save=False,
    )


message = st.chat_input("Send a message to the ai ")

if message:
    send_message(message, "human")
    time.sleep(2)
    send_message(f"You said: {message}", "ai")

    with st.sidebar:
        st.write(st.session_state)