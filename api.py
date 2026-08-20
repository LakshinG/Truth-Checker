from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from src.vector_store import VectorStoreManager
from src.critic import CriticAgent

load_dotenv()

app = FastAPI(title="Research Paper Truth-Checker API")

# Initialize components globally so they are ready for requests
try:
    vector_manager = VectorStoreManager(persist_directory="./chroma_db")
    critic = CriticAgent()
except Exception as e:
    print(f"Initialization error: {e}")
    vector_manager = None
    critic = None

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    critique: str
    num_documents_retrieved: int

@app.get("/health")
async def health_check():
    """Health check endpoint for AWS Target Groups/Load Balancers."""
    return {"status": "healthy", "components_loaded": vector_manager is not None}

@app.post("/query", response_model=QueryResponse)
async def check_truth(request: QueryRequest):
    """Query the truth-checker agent with a claim."""
    if not os.getenv("GOOGLE_API_KEY"):
         raise HTTPException(status_code=500, detail="GOOGLE_API_KEY not configured in environment")
    
    if vector_manager is None or critic is None:
         raise HTTPException(status_code=500, detail="AI components failed to initialize")

    try:
        # Fall back to standard vector search (BM25 requires in-memory corpus loaded during ingest)
        retriever = vector_manager.get_vector_retriever(k=4)
        retrieved_docs = retriever.invoke(request.query)
        
        # Run through Critic Agent
        state = {"query": request.query, "documents": retrieved_docs, "critique": ""}
        result = critic.analyze(state)
        
        return QueryResponse(
            query=request.query,
            critique=result.get("critique", "No critique generated."),
            num_documents_retrieved=len(retrieved_docs)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
