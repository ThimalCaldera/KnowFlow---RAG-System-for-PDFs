import os
import streamlit as st
import streamlit_scrollable_textbox as stx
import PyPDF2
import tempfile
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv, find_dotenv


_ = load_dotenv(find_dotenv()) # read local .env file

API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=API_KEY)


def load_db(file, chain_type, k):
    
    loader = PyPDFLoader(file) # load documents
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000000, chunk_overlap=150) # split documents
    docs = text_splitter.split_documents(documents)
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001") # define embedding
    
    db = DocArrayInMemorySearch.from_documents(docs, embeddings) # create vector database from data
    
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": k}) # define retriever
    
    # create a chatbot chain. Memory is managed externally.
    
    qa = ConversationalRetrievalChain.from_llm(
        llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature = 0,convert_system_message_to_human=True), 
        chain_type=chain_type, 
        retriever=retriever, 
        return_source_documents=True,
        return_generated_question=True,
    )
    return qa 

# Streamlit GUI 

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.title("💡:red[KnowFlow] - :green[Chat-Driven Document Navigation]")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
print(uploaded_file)


if uploaded_file is not None:
   
    st.success('PDF File Uploaded Successfully !!', icon="✅")

    # Save the uploaded file to a temporary location
    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(temp_dir, "uploaded_file.pdf")
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(uploaded_file.getvalue())

    # Load the document and create the chatbot chain
    qa = load_db(temp_file_path, "stuff", 10)

    # User input for chatbot
    query = st.text_input("Ask a question:")
    
    if st.button("Submit"):
        
        result = qa({"question": query, "chat_history": st.session_state.chat_history})
        st.session_state.chat_history.extend([(query, result["answer"])])
        st.toast("Response generated!", icon='🎉')
        
        st.markdown("<b>Answer:</b>", unsafe_allow_html=True)
        st.markdown(f"<div style='border: 1px solid #ccc; padding: 10px; border-radius: 5px; font-size: 16px;'>{result['answer']}</div>", unsafe_allow_html=True)
    
        st.write("\n\n")
        st.markdown("<b>Chat History:</b>", unsafe_allow_html=True)
        chat_history_text = ""   
            
        for user, bot in reversed(st.session_state.chat_history):  # Reverse the list
            chat_history_text += f"User:   {user}\n"
            chat_history_text += f"Bot:   {bot}\n\n"
            
        stx.scrollableTextbox(chat_history_text, height = 300)
    
else:
    st.write("Please upload a PDF file.")
 
 
# Create footer for the application    
footer="""<style>
a:link , a:visited{
color: red;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: black;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p> 🚀 Built with Streamlit by <a href = "https://github.com/ThimalCaldera"  target="blank">Thimal Caldera </a> | 📚 Powered by Gemini-Pro</p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)

