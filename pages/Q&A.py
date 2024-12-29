import streamlit as st
import os
import datetime
import json
import time
import mysql.connector
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

os.environ['HF_TOKEN'] = os.getenv("HF_TOKEN")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-8b-8192")

prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Provide the most accurate response based on the question:
    <context>
    {context}
    <context>
    Question: {input}
    """
)

def connect_sql_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="hello"
        )
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS document_responses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_prompt TEXT,
            answer TEXT,
            context TEXT,
            created_at DATETIME
        )
        ''')
        return conn, cursor
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None, None

def insert_into_sql_db(user_prompt, answer, context):
    conn, cursor = connect_sql_db()
    if conn is None:
        return
    created_at = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO document_responses (user_prompt, answer, context, created_at)
        VALUES (%s, %s, %s, %s)
    ''', (user_prompt, answer, json.dumps(context), created_at))
    conn.commit()
    conn.close()

def fetch_from_sql_db(document_id):
    conn, cursor = connect_sql_db()
    if conn is None:
        return None
    cursor.execute("SELECT * FROM document_responses WHERE id = %s", (document_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def create_vector_embedding():
    if "vectors" not in st.session_state:
        try:
            st.session_state.loader = PyPDFDirectoryLoader("C:/Users/chafl/OneDrive/Desktop/done/pages/papers")
            st.session_state.docs = st.session_state.loader.load()

            if not st.session_state.docs:
                st.error("No documents found in the directory. Add some PDFs.")
                return

            st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:50])

            st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, embeddings)
            st.success("Vector Database is ready!")
        except Exception as e:
            st.error(f"An error occurred: {e}")

st.title("RAG Document Q&A with Groq and SQL Database")

user_prompt = st.text_input("Enter your query from the research papers")

if st.button("Create Document Embedding"):
    create_vector_embedding()

if user_prompt:
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = st.session_state.vectors.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    start_time = time.process_time()
    response = retrieval_chain.invoke({'input': user_prompt})
    st.write(response['answer'])

    try:
        context = [doc.page_content for doc in response['context']]
        insert_into_sql_db(user_prompt, response['answer'], context)
        st.success("Response saved to SQL Database!")
    except Exception as e:
        st.error(f"Error saving to SQL Database: {e}")

    with st.expander("Similar Documents"):
        for i, doc in enumerate(response['context']):
            st.write(doc.page_content)
            st.write("------------------------")

st.header("Fetch Data from SQL Database")

document_id = st.text_input("Enter Document ID (SQL)")
if st.button("Fetch Response"):
    try:
        result = fetch_from_sql_db(document_id)
        if result:
            st.json({
                "user_prompt": result[1],
                "answer": result[2],
                "context": json.loads(result[3]),
                "created_at": result[4]
            })
        else:
            st.error("No document found with that ID.")
    except Exception as e:
        st.error(f"Error fetching document: {e}")
