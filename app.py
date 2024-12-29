import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
import openai

from dotenv import load_dotenv
load_dotenv()

# Set up environment variables
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
os.environ['HF_TOKEN'] = os.getenv("HF_TOKEN")
from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-8b-8192")

# Define prompt templates
prompt1 = ChatPromptTemplate.from_template("""
    the user will 
    <context>
    {context}
    <context>
    Question:{input}
""")

prompt = ChatPromptTemplate.from_template("""
    tell if the entered context is either based on sql query 
    or based on natural language query
    or general question
    <context>
    {context}
    <context>
    Question:{input}
""")

# Function to create vector embedding from documents
def create_vector_embedding():
    if "vectors" not in st.session_state:
        st.session_state.embeddings = embeddings
        st.session_state.loader = PyPDFDirectoryLoader("C:/Users/chafl/OneDrive/Desktop/done/pages/papers")
        
        # Load documents
        st.session_state.docs = st.session_state.loader.load()
        
        if not st.session_state.docs:
            st.error("No documents found in the 'papers' directory. Please add some PDFs.")
            return
        
        # Split documents
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        st.session_state.final_docs = st.session_state.text_splitter.split_documents(
            st.session_state.docs[:min(50, len(st.session_state.docs))]
        )
        
        # Create vector store
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_docs, st.session_state.embeddings)
        st.success("Vector Database is ready!")

# Streamlit UI setup
st.set_page_config(page_title="Multi-Page Example")

# Sidebar navigation
page_selection = st.sidebar.radio(
    "Select a Page",
    ("Home", "SQL Query Answer", "Q&A with Documents", "Transformers Question")
)

# Page for SQL Query Answer
def sql_query_page():
    st.subheader("SQL Query Section")
    user_prompt_sql = st.text_input("Enter your SQL Query")
    if st.button("Answer SQL Query"):
        # Handle the SQL query logic here
        st.write("SQL Query Answer: This is where the SQL query response would be displayed.")

# Page for Q&A with Documents
def qa_with_documents_page():
    st.subheader("Q&A with Documents Section")
    user_prompt_qa = st.text_input("Enter your Problem statement")
    if st.button("Get Answer"):
        document_chain = create_stuff_documents_chain(llm, prompt)
        retriever = st.session_state.vectors.as_retriever()
        retrieval_chain = create_retrieval_chain(retriever, document_chain)

        import time
        start = time.process_time()
        response = retrieval_chain.invoke({'input': user_prompt_qa})
        st.write(f"Response time : {time.process_time() - start}")

        st.write(response['answer'])

        with st.expander("Document similarity Search"):
            for i, doc in enumerate(response['context']):
                st.write(doc.page_content)
                st.write('------------------------')

# Page for Transformers Question
def transformers_page():
    st.subheader("Transformers Question Section")
    user_prompt_transformer = st.text_input("Enter your question for Transformers")
    if st.button("Ask Transformer"):
        # Add logic to interact with transformer models here
        st.write("Transformer Answer: This is where the transformer-based answer would be displayed.")

# Display the selected page
if page_selection == "SQL Query Answer":
    sql_query_page()
elif page_selection == "Q&A with Documents":
    qa_with_documents_page()
elif page_selection == "Transformers Question":
    transformers_page()
else:
    st.title("Welcome to the Multi-Page App")
    st.write("Use the sidebar to navigate through different sections.")




import requests


def call_api_for_qa(user_prompt):
    try:
        # Define the endpoint and parameters for the API request
        api_url = "http://localhost:8501/Q&A"
        
        # You can send data with the request as a JSON or form data
        payload = {
            "user_prompt": user_prompt  # The data you want to send
        }

        # Making a POST request to the API
        response = requests.post(api_url, json=payload)

        # Check the response status
        if response.status_code == 200:
            # Successfully received the response
            return response.json()  # This assumes the API returns JSON data
        else:
            # Handle errors (e.g., API is down or returns an error)
            st.error(f"API call failed with status code {response.status_code}")
            return None
    
    except requests.exceptions.RequestException as e:
        # Handle connection errors or timeout errors
        st.error(f"Error making API request: {e}")
        return None

# Example usage in your Streamlit app
st.title("API Integration Example")

# Input box for the user to enter their prompt
user_prompt = st.text_input("Enter your question for Q&A")

if st.button("Ask Q&A"):
    if user_prompt:
        # Call the API with the user prompt
        response = call_api_for_qa(user_prompt)
        
        if response:
            # Display the response from the API (if any)
            st.write("Response from API:")
            st.write(response)
        else:
            st.write("No response from the API.")

