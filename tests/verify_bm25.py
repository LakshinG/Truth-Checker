import shutil
import os
from unittest.mock import MagicMock
from src.vector_store import VectorStoreManager
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

class MockEmbeddings(Embeddings):
    def embed_documents(self, texts):
        return [[0.1] * 1536 for _ in texts]
    def embed_query(self, text):
        return [0.1] * 1536

if __name__ == "__main__":
    docs = [
        Document(page_content="The sun rises in the east.", metadata={"id": 1}),
        Document(page_content="The moon orbits the earth.", metadata={"id": 2})
    ]
    
    bm25 = BM25Retriever.from_documents(docs)
    bm25.k = 2
    results = bm25.invoke("sun")
    print("BM25 Results:")
    for doc in results:
        print(f"  {doc.page_content}")
        
    manager = VectorStoreManager(persist_directory="./chroma_db_test", embedding_model=MockEmbeddings())
    manager.add_documents(docs)
    vector_retriever = manager.get_vector_retriever(k=2)
    results_v = vector_retriever.invoke("sun")
    print("Vector Results:")
    for doc in results_v:
        print(f"  {doc.page_content}")

    if os.path.exists("./chroma_db_test"):
        shutil.rmtree("./chroma_db_test")
