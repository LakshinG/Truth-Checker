import os
from typing import List, Dict, Optional
from langchain_community.document_loaders import PyPDFLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

class IngestionPipeline:
    def __init__(self, embedding_model=None):
        """
        Initialize the ingestion pipeline.
        
        Args:
            embedding_model: The embedding model to use for semantic chunking.
                             Defaults to OpenAIEmbeddings if not provided.
        """
        self.embedding_model = embedding_model or OpenAIEmbeddings()
        # SemanticChunker uses the embedding model to determine breakpoints
        self.text_splitter = SemanticChunker(self.embedding_model)

    def load_pdf(self, file_path: str) -> List[Document]:
        """Loads a PDF file and returns a list of Documents."""
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return documents

    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Splits documents into semantic chunks."""
        chunks = self.text_splitter.split_documents(documents)
        return chunks

    def _extract_metadata_from_filename(self, filename: str) -> Dict:
        """
        Heuristic to extract metadata from filename.
        Expected format: Author_Year_DOI.pdf or just simple processing.
        This is a placeholder for more complex logic.
        """
        # Remove extension
        name = os.path.splitext(filename)[0]
        parts = name.split('_')
        
        metadata = {}
        if len(parts) >= 3:
            metadata['author'] = parts[0]
            metadata['year'] = parts[1]
            metadata['doi'] = parts[2]
        else:
            metadata['title'] = name
            
        return metadata

    def process_file(self, file_path: str, metadata: Optional[Dict] = None) -> List[Document]:
        """
        Loads a PDF, chunks it, and applies metadata.
        """
        raw_docs = self.load_pdf(file_path)
        
        file_metadata = metadata or self._extract_metadata_from_filename(os.path.basename(file_path))
        
        # Update metadata for all pages
        for doc in raw_docs:
            doc.metadata.update(file_metadata)
            
        chunks = self.chunk_documents(raw_docs)
        
        # Ensure metadata is preserved/propagated (SemanticChunker usually does this)
        # But we can double check or enforce specific tags
        for chunk in chunks:
            # chunk.metadata is already a copy of the original doc metadata + some splitter info
            pass
            
        return chunks

    def ingest_directory(self, directory_path: str) -> List[Document]:
        """Ingests all PDFs in a directory."""
        all_chunks = []
        if not os.path.exists(directory_path):
            print(f"Directory {directory_path} does not exist.")
            return []

        for filename in os.listdir(directory_path):
            if filename.lower().endswith(".pdf"):
                file_path = os.path.join(directory_path, filename)
                print(f"Processing {filename}...")
                try:
                    chunks = self.process_file(file_path)
                    all_chunks.extend(chunks)
                    print(f"  Generated {len(chunks)} chunks.")
                except Exception as e:
                    print(f"  Error processing {filename}: {e}")
                    
        return all_chunks
