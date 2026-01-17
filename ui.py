import streamlit as st
import os
from main import run_ingestion, run_query  # Assuming these are your entry functions

# 1. Page Configuration
st.set_page_config(page_title="Research Truth-Checker", layout="wide")
st.title("🔬 Research Paper Truth-Checker")
st.markdown("Analyze multiple research papers for methodological contradictions.")

# 2. Sidebar for Configuration
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini/OpenAI API Key", type="password")
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key  # Or OPENAI_API_KEY
    
    st.divider()
    st.info("This system uses RAG and a 'Critic Agent' to identify discrepancies in research findings.")

# 3. File Upload Section
st.subheader("1. Upload Research Papers")
uploaded_files = st.file_uploader(
    "Upload PDFs for analysis", 
    type="pdf", 
    accept_multiple_files=True
)

if st.button("Ingest Papers") and uploaded_files:
    with st.spinner("Processing and chunking PDFs..."):
        # Save uploaded files temporarily for your ingestion logic
        temp_dir = "temp_pdf_storage"
        os.makedirs(temp_dir, exist_ok=True)
        for uploaded_file in uploaded_files:
            with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
        
        # Call your existing ingestion function
        num_chunks = run_ingestion(temp_dir) 
        st.success(f"Ingested {num_chunks} chunks into the Vector Store!")

# 4. Query & Analysis Section
st.subheader("2. Run Contradiction Analysis")
user_query = st.text_input("Enter your research question (e.g., 'Does coffee improve performance?')")

if st.button("Analyze") and user_query:
    if not api_key:
        st.error("Please enter an API Key in the sidebar.")
    else:
        with st.spinner("Retrieving context and running Critic Agent..."):
            # Call your existing query function
            analysis_output = run_query(user_query)
            
            st.divider()
            st.markdown("### --- Critic Analysis ---")
            st.write(analysis_output)