import os
import argparse
from typing import List
from dotenv import load_dotenv
from langchain_core.documents import Document

# Import modules
from src.ingestion import IngestionPipeline
from src.vector_store import VectorStoreManager
from src.critic import CriticAgent

load_dotenv()

# --- MODULAR FUNCTIONS FOR UI AND TERMINAL ---

def run_ingestion(directory: str, persist_dir: str = "./chroma_db"):
    """Handles PDF processing and storage."""
    ingestion = IngestionPipeline()
    vector_manager = VectorStoreManager(persist_directory=persist_dir)
    
    print(f"Ingesting from {directory}...")
    chunks = ingestion.ingest_directory(directory)
    
    if chunks:
        vector_manager.add_documents(chunks)
        print(f"Ingested {len(chunks)} chunks.")
        return len(chunks), chunks
    return 0, []

def run_query(query_text: str, documents_for_bm25: List[Document] = None, persist_dir: str = "./chroma_db"):
    """Handles retrieval and critic agent analysis."""
    vector_manager = VectorStoreManager(persist_directory=persist_dir)
    
    # Retrieval Strategy
    if documents_for_bm25:
        print("Using Hybrid Search (Vector + BM25)")
        retriever = vector_manager.create_hybrid_retriever(documents_for_bm25, k=4)
    else:
        print("Using Vector Search (BM25 unavailable without corpus in memory)")
        retriever = vector_manager.get_vector_retriever(k=4)
        
    retrieved_docs = retriever.invoke(query_text)
    
    # Critic Agent Logic
    critic = CriticAgent()
    state = {"query": query_text, "documents": retrieved_docs, "critique": ""}
    result = critic.analyze(state)
    return result["critique"]

# --- TERMINAL ENTRY POINT ---

def main():
    parser = argparse.ArgumentParser(description="Research Paper Truth-Checker")
    parser.add_argument("--ingest", type=str, help="Directory to ingest PDFs from")
    parser.add_argument("--query", type=str, help="Query to check")
    parser.add_argument("--persist-dir", type=str, default="./chroma_db", help="ChromaDB persistence directory")
    args = parser.parse_args()
    
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
        print("Warning: No API Keys found.")
    
    docs_in_memory = []
    
    if args.ingest:
        _, docs_in_memory = run_ingestion(args.ingest, args.persist_dir)
    
    if args.query:
        result = run_query(args.query, docs_in_memory, args.persist_dir)
        print("\n--- Critic Analysis ---")
        print(result)

if __name__ == "__main__":
    main()