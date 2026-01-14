from unittest.mock import MagicMock
from src.ingestion import IngestionPipeline
from langchain_core.embeddings import Embeddings

class MockEmbeddings(Embeddings):
    def embed_documents(self, texts):
        # Return a dummy embedding for each text
        return [[0.1] * 1536 for _ in texts]
    def embed_query(self, text):
        return [0.1] * 1536

if __name__ == "__main__":
    pipeline = IngestionPipeline(embedding_model=MockEmbeddings())
    docs = pipeline.process_file("Doe_2023_10.1234.pdf")
    print(f"Processed {len(docs)} chunks.")
    if len(docs) > 0:
        print("Metadata:", docs[0].metadata)
        print("Content sample:", docs[0].page_content[:50])
