import os
import argparse
from typing import List
from dotenv import load_dotenv
from langchain_core.documents import Document

# Import modules
from src.ingestion import IngestionPipeline
from src.vector_store import VectorStoreManager
from src.critic import CriticAgent

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Research Paper Truth-Checker")
    parser.add_argument("--ingest", type=str, help="Directory to ingest PDFs from")
    parser.add_argument("--query", type=str, help="Query to check")
    parser.add_argument("--persist-dir", type=str, default="./chroma_db", help="ChromaDB persistence directory")
    args = parser.parse_args()
    
    # Check for API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not found. Operations requiring LLM will fail unless mocked or key is provided.")
    
    # Initialize components
    # We might need to handle the case where keys are missing by allowing the user to proceed if they are running a test/mock setup,
    # but strictly speaking, the main app expects keys.
    try:
        ingestion = IngestionPipeline()
        vector_manager = VectorStoreManager(persist_directory=args.persist_dir)
    except Exception as e:
        print(f"Initialization error (check API keys): {e}")
        return

    documents_for_bm25 = []

    # Ingestion Phase
    if args.ingest:
        print(f"Ingesting from {args.ingest}...")
        chunks = ingestion.ingest_directory(args.ingest)
        if chunks:
            vector_manager.add_documents(chunks)
            documents_for_bm25 = chunks
            print(f"Ingested {len(chunks)} chunks.")
        else:
            print("No PDF files found or processed.")
    
    # Query Phase
    if args.query:
        print(f"\nProcessing Query: {args.query}")
        
        # Retrieval Strategy
        # Ideally we use Hybrid, but we need the corpus for BM25.
        # If we just ingested, we have 'documents_for_bm25'.
        # If not, we fall back to Vector Search.
        
        if documents_for_bm25:
            print("Using Hybrid Search (Vector + BM25)")
            retriever = vector_manager.create_hybrid_retriever(documents_for_bm25, k=4)
        else:
            print("Using Vector Search (BM25 unavailable without corpus in memory)")
            retriever = vector_manager.get_vector_retriever(k=4)
            
        try:
            retrieved_docs = retriever.invoke(args.query)
            print(f"Retrieved {len(retrieved_docs)} relevant contexts.")
            
            # Critic Agent
            critic = CriticAgent()
            state = {"query": args.query, "documents": retrieved_docs, "critique": ""}
            result = critic.analyze(state)
            
            print("\n--- Critic Analysis ---")
            print(result["critique"])
            
        except Exception as e:
            print(f"Error during execution: {e}")

if __name__ == "__main__":
    main()
