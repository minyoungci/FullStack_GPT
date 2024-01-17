import streamlit as st 
import time

from typing import Text

from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings
from langchain.vectorstores import FAISS
from langchain.storage import LocalFileStore
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda


st.set_page_config(
    page_title = 'DocumentGPT',
    page_icon='🧊',
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

def send_message(message, role, save=True):
    with st.chat_message(role):
        st.markdown(message)
    if save:
        st.session_state['messages'].append({"message":message, "role":role})

def paint_history():
    for message in st.session_state['messages']:
        send_message(message["message"], message["role"], save=False)

st.title("DocumentGPT")

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
        send_message("lalalal", "ai")

else: 
    st.session_state['messages'] = [] # 파일이 변경되었을 경우 채팅 기록 초기화 