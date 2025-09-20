from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from database import get_connection, get_designation, get_name
from config import LOGIN_URL, SIGNUP_URL, retrieve_clevel, retrieve_eng, retrieve_fin, retrieve_gen, retrieve_hr, retrieve_mark
import streamlit as st 
import requests
from dotenv import load_dotenv
load_dotenv()

# model define
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    task="text_generation",
    timeout=120
    )

model = ChatHuggingFace(llm=llm)

prompt = PromptTemplate(
                        template= """
                                you are a assistant of a comapany and you have that understanding of the you will only answer the below question
                                from the below context, if the context is not enough, then answer that the limited knowledge:
                                context : {context}
                                question : {question}
                                """,
                        input_variables=["role", "context", "question"]

                        )

parser = StrOutputParser()

chain = prompt | model | parser


# streamlit app

st.title("FinSolve Technologies")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "designation" not in st.session_state:
    st.session_state.designation = None
if "name" not in st.session_state:
    st.session_state.name = None
if "messages" not in st.session_state:
    st.session_state.messages = []



if not st.session_state.authenticated:
    st.session_state.messages = []
    auth = st.radio("Choose option: ", ["Login", "Sign Up"], index = 0)
    if auth == "Sign Up":
        name = st.text_input("Name")
        designation = st.selectbox("Department", ["Marketing", "Finance", "HR", "Engineering", "general", "C-level"])
    else:
        name = None
        designation = None
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if auth == "Sign Up" and st.button("Sign Up"):
        if len(password) < 8:
            st.error("Password must be at least 8 character")
        elif len(username.split()) !=1:
            st.error("Space not allowed in the username")
        else:
            user_input = {
                    'username':username,
                    'name': name,
                    'designation': designation,
                    'password': password
                    }
            response = requests.post(SIGNUP_URL, json = user_input)
            if response.status_code == 200:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.designation = designation
                st.session_state.name = name
                st.success("Registration Successfully")
            else:
                st.error("Username already exists")

    if auth == "Login" and st.button("Log in"):
        if len(username)==0:
            st.error("Input username")
        elif len(password)==0:
            st.error("Enter password")
        else:
            user_input = {
                        "username": username,
                        "password": password
            }
            response = requests.post(LOGIN_URL, json=user_input)
            if response.status_code == 200:
                st.session_state.authenticated = True
                st.session_state.username = username
                conn = get_connection()
                st.session_state.designation = get_designation(conn, username)
                conn = get_connection()
                st.session_state.name = get_name(conn, username)
                st.success("Log in Successfully")
            else:
                st.error("Wrong Credential")

if st.session_state.authenticated:
    col1, col2= st.columns([3,1])

    with col1:
        st.subheader(st.session_state.designation +  " Team")
        st.subheader(f"Welcome {st.session_state.name}")
    
    with col2:
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.designation = None
            st.session_state.name = None
            st.session_state.username = None
            st.rerun()
        
    for msg in st.session_state.messages:
        _, _, right = st.columns([2,1,8])
        left, _, _ = st.columns([8,1,2])
        if msg["role"] == "user":
            with right:
                with st.chat_message('user'):
                    st.markdown(msg['content'])
        else:
            with left:
                with st.chat_message('assistant'):
                    st.markdown(msg['content'])

    if question := st.chat_input("Say Something"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": question})
        _, _, right = st.columns([2, 1, 8])
        with right:
            st.chat_message("user").markdown(question)


        if st.session_state.designation == "Marketing":
            context = retrieve_mark.invoke(question)
           
        elif st.session_state.designation == "Finance":
            context = retrieve_fin.invoke(question)
            
        elif st.session_state.designation == "Engineering":
            context = retrieve_eng.invoke(question)
           
        elif st.session_state.designation == "HR":
            context = retrieve_hr.invoke(question)
          
        elif st.session_state.designation=="general":
            context = retrieve_gen.invoke(question)

        else:
            context = retrieve_clevel.invoke(question)

        context = "\n\n".join(doc.page_content for doc in context)
        response = chain.invoke({"question":question, "context": context})
        st.session_state.messages.append({"role": "assistant", "content": response})
        left,_, _ = st.columns([8, 1, 1])
        with left:
            st.chat_message("assistant").markdown(response)
          





