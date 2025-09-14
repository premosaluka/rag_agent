"""
vectorstore.py: Load articles to documents, chunk documents, embed, store in ChromaDB vectorstore
"""
import os

import CONFIG as C
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

data_folder = C.VECTOR_STORE_DATA_FOLDER
vectorstore_folder = C.VECTOR_STORE_DB_FOLDER
embedding_model = C.VECTOR_STORE_EMBEDDING_MODEL

def load_vectorstore():
    print('Starting database build')

    # Load documents
    all_docs = []
    for filename in os.listdir(data_folder):
        # Check if it's a file (not a folder)
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(data_folder, filename))
            docs = loader.load()
            all_docs.extend(docs)
            #continue
        break
    print(f'Documents read: Nr {len(all_docs)}.')

    # Split documents into chunks
    print('Splitting documents.')
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=800, chunk_overlap=200)
    doc_splits = splitter.split_documents(all_docs)

    print('Starting DB build.')
    # Embed and store in FAISS
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name="VET-RAG-chroma",
        embedding=OpenAIEmbeddings(model=embedding_model),
        persist_directory=vectorstore_folder,
     )
    return vectorstore

retriever = Chroma(
    collection_name="VET-RAG-chroma",
    persist_directory=vectorstore_folder,
    embedding_function=OpenAIEmbeddings(model=embedding_model),
).as_retriever()