import os
from reportlab.pdfgen import canvas
from unittest.mock import MagicMock
from src.ingestion import IngestionPipeline
from langchain_core.embeddings import Embeddings

def create_dummy_pdf(filename):
    c = canvas.Canvas(filename)
    c.drawString(100, 750, "This is a test research paper.")
    c.drawString(100, 730, "It contains some claims about the world.")
    c.drawString(100, 710, "Author: John Doe. Year: 2023.")
    c.save()

class MockEmbeddings(Embeddings):
    def embed_documents(self, texts):
        # Return a dummy embedding for each text
        return [[0.1] * 1536 for _ in texts]
    def embed_query(self, text):
        return [0.1] * 1536

if __name__ == "__main__":
    filename = "Doe_2023_10.1234.pdf"
    create_dummy_pdf(filename)
    try:
        pipeline = IngestionPipeline(embedding_model=MockEmbeddings())
        docs = pipeline.process_file(filename)
        print(f"Processed {len(docs)} chunks.")
        if len(docs) > 0:
            print("Metadata:", docs[0].metadata)
            print("Content sample:", docs[0].page_content[:50])
    finally:
        if os.path.exists(filename):
            os.remove(filename)
