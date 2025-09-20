from vectorstore import load_clevel, load_eng, load_fin, load_gen, load_hr, load_mark

#Url
LOGIN_URL = "http://127.0.0.1:8000/login"
SIGNUP_URL = "http://127.0.0.1:8000/signup"

#vector store
vector_clevel = load_clevel(r"D:\Desktop\langchain\RAG_A\data")
vector_mark= load_mark(r"D:\Desktop\langchain\RAG_A\data\marketing")
vector_eng = load_eng(r"D:\Desktop\langchain\RAG_A\data\engineering")
vector_hr = load_hr(r"D:\Desktop\langchain\RAG_A\data\hr")
vector_gen = load_gen(r"D:\Desktop\langchain\RAG_A\data\general")
vector_fin = load_fin(r"D:\Desktop\langchain\RAG_A\data\finance")

retrieve_clevel = vector_clevel.as_retriever(search = "similarity", search_kwags={"k":3})
retrieve_mark=vector_mark.as_retriever(search="similarity", search_kwags={"k":4})
retrieve_eng = vector_eng.as_retriever(search= "similarity", search_kwags= {"k":4})
retrieve_hr = vector_hr.as_retriever(search="similarity", search_kwags={"k":100})
retrieve_gen = vector_gen.as_retriever(search="similarity", search_kwags={"k":4})
retrieve_fin = vector_fin.as_retriever(search= "similarity", search_kwags= {"k":4})
