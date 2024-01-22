from uuid import UUID
import streamlit as st 
import time

from typing import Any, Dict, List, Optional, Text

from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.storage import LocalFileStore
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.callbacks.base import BaseCallbackHandler

st.set_page_config(
    page_title = 'PrivateGPT',
    page_icon='🧊',
)

class ChatCallBackHandler(BaseCallbackHandler):

    message = ""

    def on_llm_start(self, *args, **kwargs): 
        self.message_box = st.empty()

    def on_llm_end(self, *args, **kwargs): 
        save_message(self.message, "ai")

    def on_llm_new_token(self, token: str, *args, **kwargs):
        self.message += token
        self.message_box.markdown(self.message)


llm = ChatOpenAI(
    temperature=0.1,
    streaming=True, # 실시간으로 출력결과 콘솔에 보여줌
    callbacks = [
        ChatCallBackHandler(),
    ]
)

if "messages" not in st.session_state:
    st.session_state['messages'] = []

@st.cache_data(show_spinner="Embedding file...") # file이 동일하다면 streamlit은 이 함수를 재실행시키지 않는다. 처음에만 실행되고 두 번째에는 파일이 변경되지 않으면 실행하지 않음. 
def embed_file(file):
    file_content = file.read()
    file_path = f"./.cache/files/{file.name}"

    with open(file_path, "wb") as f:
        f.write(file_content)
        cache_dir = LocalFileStore(f"./.cache/embeddings/{file.name}")

    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\n",
        chunk_size=600,
        chunk_overlap=100,
    )
    loader = UnstructuredFileLoader(file_path)
    docs = loader.load_and_split(text_splitter=splitter)
    embeddings = OpenAIEmbeddings()
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, cache_dir)
    vectorstore = FAISS.from_documents(docs, cached_embeddings)
    retriever = vectorstore.as_retriever()
    return retriever

def save_message(message, role):
        st.session_state['messages'].append({"message":message, "role":role})


def send_message(message, role, save=True):
    with st.chat_message(role):
        st.markdown(message)
    if save:
        save_message(message, role) 

def paint_history():
    
    for message in st.session_state['messages']:
        send_message(message["message"], message["role"], save=False)

def format_docs(docs):
    return "\n\n".join(document.page_content for document in docs)

prompt = ChatPromptTemplate.from_messages([
    ("system", """
        Answer the question using ONLY the following context. If you don't know the answer just say you don't know. DON'T make anythin up.
     
     Context: {context}
     """
    ),
    ("human", "{question}"),
])

st.title("Minyoung GPT")

st.markdown(
    """
welcome ! 
            
Use this chatbot to ask questions to an AI about your files! 

Upload your file on sidebar ! 
"""
)

with st.sidebar:
    file = st.file_uploader("Upload a file",
                         type=["pdf", "txt", "docx"])

if file:
    retriever = embed_file(file)    
    send_message("I'm ready! Ask me anything!", "ai", save=False)
    paint_history()
    message = st.chat_input("Ask anything about your file...")
    if message:
        send_message(message, "human")
        chain = ({
            "context":retriever | RunnableLambda(format_docs),
            "question" : RunnablePassthrough(),
        } 
        | prompt 
        | llm 
        ) 
        with st.chat_message("ai"):
            response = chain.invoke(message)

else: 
    st.session_state['messages'] = [] # 파일이 변경되었을 경우 채팅 기록 초기화 