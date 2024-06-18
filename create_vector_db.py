from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key= os.getenv("GOOGLE_API_KEY"))
pdf_data_path = f"./data_source"
vector_db_path = "vector_index"
def create_db_from_files():
    #Tìm kiếm và đọc file dữ liệu
    loader = DirectoryLoader(pdf_data_path, glob="*.pdf", loader_cls = PyPDFLoader)
    documents = loader.load()
    #Chia nhỏ văn bản
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    # Embedding
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_index = Chroma.from_documents(chunks, embedding_model,persist_directory= vector_db_path)
    vector_index.persist()
    return vector_index

create_db_from_files()
