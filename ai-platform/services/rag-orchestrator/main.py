from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import sys

# Import the shared logger
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
try:
    from shared.logger.logging_config import logger
except ImportError:
    import logging
    logger = logging.getLogger("ai_platform.rag_orchestrator")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    logger.addHandler(handler)

from orchestrator import RAGOrchestrator

app = FastAPI()

# Initialize the orchestrator
orchestrator = RAGOrchestrator()

# Define data models
class RAGRequest(BaseModel):
    query: str
    collection_name: str
    n_results: int = 5

@app.get("/health")
def read_health():
    """Health check endpoint"""
    return {"status": "ok"}

@app.post("/rag")
async def process_rag_query(request: RAGRequest):
    """
    Process a query through the RAG pipeline.
    """
    try:
        result = await orchestrator.process_query(
            query=request.query,
            collection_name=request.collection_name,
            n_results=request.n_results
        )
        return result
    except Exception as e:
        logger.error(f"Error processing RAG query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/collections")
async def list_collections():
    """
    List all available collections.
    """
    try:
        collections = await orchestrator.list_collections()
        return {"collections": collections}
    except Exception as e:
        logger.error(f"Error listing collections: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
