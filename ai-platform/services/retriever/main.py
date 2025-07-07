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
    logger = logging.getLogger("ai_platform.retriever")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    logger.addHandler(handler)

from retriever import Retriever

app = FastAPI()

# Initialize the retriever
retriever = Retriever()

# Define data models
class RetrieveRequest(BaseModel):
    query: str
    collection_name: str
    n_results: int = 5

class CollectionRequest(BaseModel):
    collection_name: str

@app.get("/health")
def read_health():
    """Health check endpoint"""
    return {"status": "ok"}

@app.post("/retrieve")
async def retrieve_documents(request: RetrieveRequest):
    """
    Retrieve relevant documents for a query.
    """
    try:
        documents = await retriever.retrieve(
            query=request.query,
            collection_name=request.collection_name,
            n_results=request.n_results
        )
        return {"documents": documents}
    except Exception as e:
        logger.error(f"Error retrieving documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/collections")
async def list_collections():
    """
    List all available collections.
    """
    try:
        collections = await retriever.list_collections()
        return {"collections": collections}
    except Exception as e:
        logger.error(f"Error listing collections: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/collections/{collection_name}")
async def get_collection_info(collection_name: str):
    """
    Get information about a collection.
    """
    try:
        info = await retriever.get_collection_info(collection_name)
        return info
    except Exception as e:
        logger.error(f"Error getting collection info: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
