from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader, CSVLoader, PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os


embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def load_eng(path):
    vector_eng = Chroma(embedding_function= embedding, collection_name= "engineering",  persist_directory= "chroma_db")

    for i in os.listdir(path):
        file_path = os.path.join(path, i)
        loader = TextLoader(file_path, encoding="utf-8")
        docs = loader.load_and_split(RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50))
        for j, doc in enumerate(docs):
            doc.metadata["topic"]="engineering"
            doc.metadata["source_file"]= i
        if not vector_eng.get()['ids']:  
            vector_eng.add_documents(docs)
    return vector_eng

def load_fin(path):
    vector_fin = Chroma(embedding_function=embedding, persist_directory="chroma_db", collection_name="finance")

    for i in os.listdir(path):
        file_path = os.path.join(path, i)
        loader = TextLoader(file_path, encoding="utf-8")
        docs = loader.load_and_split(RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 50))
        for j, doc in enumerate(docs):
            doc.metadata["topic"]="finance"
            doc.metadata["source_file"]=i
        if not vector_fin.get()['ids']:  
            vector_fin.add_documents(docs)
    return vector_fin

def load_mark(path):
    vector_mark = Chroma(embedding_function=embedding, persist_directory="chroma_db", collection_name="marketing")

    for i in os.listdir(path):
        file_path = os.path.join(path, i)
        loader = TextLoader(file_path, encoding="utf-8")
        docs = loader.load_and_split(RecursiveCharacterTextSplitter(chunk_size= 1000, chunk_overlap=50))
        for j, doc in enumerate(docs):
            doc.metadata["topic"]="marketing"
            doc.metadata["source_file"]=i
        if not vector_mark.get()['ids']:  
            vector_mark.add_documents(docs)
    return vector_mark

def load_hr(path):
    vector_hr = Chroma(embedding_function=embedding, persist_directory="chroma_db", collection_name="hr_data")

    for i in os.listdir(path):
        file_path = os.path.join(path, i)
        loader = CSVLoader(file_path, encoding="utf-8")
        docs = loader.load()
        for j, doc in enumerate(docs):
            doc.metadata["topic"]="hr"
            doc.metadata["source_file"]=i
        if not vector_hr.get()["ids"]:
            vector_hr.add_documents(docs)
    return vector_hr

def load_gen(path):
    vector_gen = Chroma(embedding_function=embedding, persist_directory="chroma_db", collection_name="general")
    for i in os.listdir(path):
        file_path = os.path.join(path, i)
        loader = TextLoader(file_path, encoding="utf-8")
        docs = loader.load_and_split(RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap= 50))
        for j, doc in enumerate(docs):
            doc.metadata["topic"]="general"
            doc.metadata["source_file"]=i
        if not vector_gen.get()["ids"]:
            vector_gen.add_documents(docs)
    return vector_gen

def load_clevel(path):
    vector_clevel = Chroma(embedding_function=embedding, persist_directory="chroma_db", collection_name="c-level")
    for i, j, k in os.walk(path):
        for file in k:
            file_path = os.path.join(i, file)
            loader = TextLoader(file_path, encoding = "utf-8")
            docs = loader.load_and_split(RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 50))
            for l, doc in enumerate(docs):
                doc.metadata["topic"]="C-Level"
                doc.metadata["source_file"]=file
    
            if not vector_clevel.get()["ids"]:
                vector_clevel.add_documents(docs)
    return vector_clevel


if __name__ == "__main__":
    vector_clevel = load_clevel(r"D:\Desktop\langchain\RAG_A\data")
    vector_mark= load_mark(r"D:\Desktop\langchain\RAG_A\data\marketing")
    vector_eng = load_eng(r"D:\Desktop\langchain\RAG_A\data\engineering")
    vector_hr = load_hr(r"D:\Desktop\langchain\RAG_A\data\hr")
    vector_gen = load_gen(r"D:\Desktop\langchain\RAG_A\data\general")
    vector_fin = load_fin(r"D:\Desktop\langchain\RAG_A\data\finance")

    retrieve_clevel = vector_clevel.as_retriever(search = "similarity", search_kwags={"k":4})
    retrieve_mark=vector_mark.as_retriever(search="similarity", search_kwags={"k":4})
    retrieve_eng = vector_eng.as_retriever(search= "similarity", search_kwags= {"k":4})
    retrieve_hr = vector_hr.as_retriever(search="similarity", search_kwags={"k":10})
    retrieve_gen = vector_gen.as_retriever(search="similarity", search_kwags={"k":4})
    retrieve_fin = vector_fin.as_retriever(search= "similarity", search_kwags= {"k":4})