import streamlit as st
from langchain.memory import ConversationBufferWindowMemory
from langchain_openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain

from langchain.indexes import VectorstoreIndexCreator
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI

openai_api_key = st.secrets["OPENAI_API_KEY"]

def get_llm():
    llm = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo", temperature=0, top_p=1)
    return llm

def get_index():  # creates and returns an in-memory vector store to be used in the application
    embeddings = OpenAIEmbeddings(api_key=openai_api_key, deployment="text-similarity-ada-001")

    pdf_path = "teste.pdf"  # assumes local PDF file with this name

    loader = PyPDFLoader(file_path=pdf_path)

    text_splitter = RecursiveCharacterTextSplitter(
        separators=[
            "\n\n",
            "\n",
            ".",
            " ",
        ],
        chunk_size=1000,  # divide into 1000-character chunks using the separators above
        chunk_overlap=100,  # number of characters that can overlap with previous chunk
    )

    index_creator = VectorstoreIndexCreator(  # create a vector store factory
        vectorstore_cls=FAISS,  # use an in-memory vector store for demo purposes
        embedding=embeddings,
        text_splitter=text_splitter,
    )

    index_from_loader = index_creator.from_loaders(
        [loader]
    )  # create an vector store index from the loaded PDF

    return index_from_loader  # return the index to be cached by the client app

def get_memory():  # create memory for this chat session
    memory = ConversationBufferWindowMemory(
        memory_key="chat_history", return_messages=True
    )  # Maintains a history of previous messages

    return memory

def get_rag_chat_response(input_text, memory, index):  # chat client function
    llm = get_llm()

    conversation_with_retrieval = ConversationalRetrievalChain.from_llm(
        llm, retriever=index.vectorstore.as_retriever(), memory=memory, verbose=True
    )

    chat_response = conversation_with_retrieval.invoke(
        {"question": input_text}
    )  # pass the user message and summary to the model

    return chat_response["answer"]
