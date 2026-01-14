import shutil
import os
from unittest.mock import MagicMock
from src.ingestion import IngestionPipeline
from src.vector_store import VectorStoreManager
from src.critic import CriticAgent
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document

class MockEmbeddings(Embeddings):
    def embed_documents(self, texts):
        return [[0.1] * 1536 for _ in texts]
    def embed_query(self, text):
        return [0.1] * 1536

def run_pipeline_test():
    db_dir = "./chroma_db_test_pipeline"
    
    if os.path.exists(db_dir):
        shutil.rmtree(db_dir)
        
    # Setup Mocks
    mock_llm = MagicMock()
    # Mock chain response
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = "Verified: Logic is sound. No contradictions found."
    
    print("Starting Pipeline Verification...")
    
    # 1. Ingestion
    print("Step 1: Ingestion")
    pipeline = IngestionPipeline(embedding_model=MockEmbeddings())
    
    # Use the dummy PDFs created earlier if available
    files = [f for f in os.listdir('.') if f.endswith('.pdf')]
    chunks = []
    if files:
        for f in files:
            print(f"  Processing {f}...")
            file_chunks = pipeline.process_file(f)
            chunks.extend(file_chunks)
    else:
        print("  No PDF files found, using dummy Document.")
        chunks = [Document(page_content="Coffee is good.", metadata={"source": "test.pdf", "author": "Test", "year": "2024"})]

    print(f"  Total chunks: {len(chunks)}")

    # 2. Vector Store
    print("Step 2: Vector Store")
    manager = VectorStoreManager(persist_directory=db_dir, embedding_model=MockEmbeddings())
    manager.add_documents(chunks)
    
    # 3. Retrieval
    print("Step 3: Retrieval")
    # Hybrid search
    retriever = manager.create_hybrid_retriever(chunks, k=2)
    docs = retriever.invoke("coffee")
    print(f"  Retrieved {len(docs)} docs.")
    if docs:
        print(f"  Top doc: {docs[0].page_content[:50]}...")
    
    # 4. Critic
    print("Step 4: Critic")
    agent = CriticAgent(llm=mock_llm)
    agent.chain = mock_chain
    
    state = {"query": "Does coffee help?", "documents": docs, "critique": ""}
    result = agent.analyze(state)
    print("  Result:", result["critique"])
    
    # Verify chain inputs
    args, _ = mock_chain.invoke.call_args
    print("  Context passed to LLM was valid:", len(args[0]['context']) > 0)
    
    # Cleanup
    if os.path.exists(db_dir):
        shutil.rmtree(db_dir)
    print("Verification Complete.")

if __name__ == "__main__":
    run_pipeline_test()
