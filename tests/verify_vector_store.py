import shutil
import os
from unittest.mock import MagicMock
from src.vector_store import VectorStoreManager
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

class MockEmbeddings(Embeddings):
    def embed_documents(self, texts):
        return [[0.1] * 1536 for _ in texts]
    def embed_query(self, text):
        return [0.1] * 1536

if __name__ == "__main__":
    if os.path.exists("./chroma_db_test"):
        shutil.rmtree("./chroma_db_test")
        
    docs = [
        Document(page_content="The sun rises in the east.", metadata={"id": 1}),
        Document(page_content="The moon orbits the earth.", metadata={"id": 2})
    ]
    
    manager = VectorStoreManager(persist_directory="./chroma_db_test", embedding_model=MockEmbeddings())
    manager.add_documents(docs)
    
    retriever = manager.create_hybrid_retriever(docs, k=2)
    results = retriever.invoke("sun")
    
    print(f"Retrieved {len(results)} documents.")
    for doc in results:
        print(f"Content: {doc.page_content}")
    
    if os.path.exists("./chroma_db_test"):
        shutil.rmtree("./chroma_db_test")
