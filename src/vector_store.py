import os
from typing import List, Optional
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
except ImportError:
    GoogleGenerativeAIEmbeddings = None
from langchain_community.retrievers import BM25Retriever
try:
    from langchain.retrievers import EnsembleRetriever
except ImportError:
    try:
        from langchain_classic.retrievers.ensemble import EnsembleRetriever
    except ImportError:
        raise ImportError("Could not import EnsembleRetriever from langchain or langchain_classic")

from langchain_core.documents import Document

class VectorStoreManager:
    def __init__(self, persist_directory="./chroma_db", embedding_model=None):
        """
        Initialize the VectorStoreManager.
        
        Args:
            persist_directory: Directory to store ChromaDB data.
            embedding_model: Embedding model to use. Defaults to OpenAIEmbeddings or GoogleGenerativeAIEmbeddings based on env.
        """
        self.persist_directory = persist_directory
        
        if embedding_model:
            self.embedding_model = embedding_model
        elif os.getenv("OPENAI_API_KEY"):
            self.embedding_model = OpenAIEmbeddings()
        elif os.getenv("GOOGLE_API_KEY"):
            if GoogleGenerativeAIEmbeddings is None:
                raise ImportError("langchain-google-genai is required for Google embeddings.")
            self.embedding_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        else:
            raise ValueError("No valid API key found for OpenAI or Google. Set OPENAI_API_KEY or GOOGLE_API_KEY.")

        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_model,
            collection_name="research_papers"
        )

    def add_documents(self, documents: List[Document]):
        """Adds documents to the vector store."""
        if not documents:
            return
        self.vectorstore.add_documents(documents)

    def get_vector_retriever(self, k=4):
        """Returns the vector store retriever."""
        return self.vectorstore.as_retriever(search_kwargs={"k": k})

    def create_hybrid_retriever(self, documents: List[Document], k=4):
        """
        Creates a hybrid retriever using BM25 and Vector Search.
        
        Args:
            documents: List of documents to initialize BM25Retriever.
            k: Number of documents to retrieve.
            
        Returns:
            EnsembleRetriever
        """
        if not documents:
            print("Warning: No documents provided for BM25. Returning Vector Retriever only.")
            return self.get_vector_retriever(k=k)

        bm25_retriever = BM25Retriever.from_documents(documents)
        bm25_retriever.k = k
        
        vector_retriever = self.get_vector_retriever(k=k)
        
        ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, vector_retriever],
            weights=[0.5, 0.5]
        )
        return ensemble_retriever
