from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import os
import sys

# Import the shared logger
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
try:
    from shared.logger.logging_config import logger
except ImportError:
    import logging
    logger = logging.getLogger("ai_platform.vector_db")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    logger.addHandler(handler)

from chroma_client import ChromaClient

app = FastAPI()

# Initialize the ChromaDB client
PERSIST_DIRECTORY = os.getenv("PERSIST_DIRECTORY", "./chroma_db")
chroma_client = ChromaClient(persist_directory=PERSIST_DIRECTORY)

# Define data models
class DocumentInput(BaseModel):
    text: str
    metadata: Optional[Dict[str, Any]] = None
    id: Optional[str] = None

class DocumentsInput(BaseModel):
    documents: List[DocumentInput]
    collection_name: str

class QueryInput(BaseModel):
    query_text: str
    collection_name: str
    n_results: int = 5

class CollectionInput(BaseModel):
    collection_name: str

@app.get("/health")
def read_health():
    """Health check endpoint"""
    return {"status": "ok"}

@app.post("/collections")
def create_collection(collection_input: CollectionInput):
    """Create a new collection"""
    try:
        collection = chroma_client.create_collection(collection_input.collection_name)
        return {"message": f"Collection '{collection_input.collection_name}' created successfully"}
    except Exception as e:
        logger.error(f"Error creating collection: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/collections")
def list_collections():
    """List all collections"""
    try:
        collections = chroma_client.list_collections()
        return {"collections": collections}
    except Exception as e:
        logger.error(f"Error listing collections: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/collections/{collection_name}")
def get_collection_info(collection_name: str):
    """Get information about a collection"""
    try:
        info = chroma_client.get_collection_info(collection_name)
        return info
    except Exception as e:
        logger.error(f"Error getting collection info: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/collections/{collection_name}")
def delete_collection(collection_name: str):
    """Delete a collection"""
    try:
        chroma_client.delete_collection(collection_name)
        return {"message": f"Collection '{collection_name}' deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting collection: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/documents")
def add_documents(documents_input: DocumentsInput):
    """Add documents to a collection"""
    try:
        # Extract document data
        documents = [doc.text for doc in documents_input.documents]
        metadatas = [doc.metadata if doc.metadata else {} for doc in documents_input.documents]
        ids = [doc.id for doc in documents_input.documents if doc.id]
        
        # If not all documents have IDs, set ids to None to auto-generate them
        if len(ids) != len(documents):
            ids = None
        
        result = chroma_client.add_documents(
            collection_name=documents_input.collection_name,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        return {"message": f"Added {len(documents)} documents to collection '{documents_input.collection_name}'"}
    except Exception as e:
        logger.error(f"Error adding documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
def query_collection(query_input: QueryInput):
    """Query a collection for similar documents"""
    try:
        results = chroma_client.query(
            collection_name=query_input.collection_name,
            query_text=query_input.query_text,
            n_results=query_input.n_results
        )
        return results
    except Exception as e:
        logger.error(f"Error querying collection: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
