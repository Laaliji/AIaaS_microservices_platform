from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import sys
import json

# Import the shared logger
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
try:
    from shared.logger.logging_config import logger
except ImportError:
    import logging
    logger = logging.getLogger("ai_platform.data_ingestion")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    logger.addHandler(handler)

from ingestion import DataIngestion
from text_splitter import TextSplitter

app = FastAPI()

# Initialize the data ingestion service
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
ingestion_service = DataIngestion(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

# Define data models
class DocumentInput(BaseModel):
    text: str
    metadata: Dict[str, Any] = {}

class BatchInput(BaseModel):
    documents: List[DocumentInput]
    collection_name: str

class CollectionInput(BaseModel):
    collection_name: str

@app.get("/health")
def read_health():
    """Health check endpoint"""
    return {"status": "ok"}

@app.post("/collections")
async def create_collection(collection_input: CollectionInput):
    """
    Create a new collection in the vector database.
    """
    try:
        result = await ingestion_service.create_collection(collection_input.collection_name)
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        return result["result"]
    except Exception as e:
        logger.error(f"Error creating collection: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
async def ingest_document(document: DocumentInput, collection_name: str):
    """
    Ingest a single document into the vector database.
    """
    try:
        result = await ingestion_service.process_document(
            text=document.text,
            metadata=document.metadata,
            collection_name=collection_name
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
            
        return result["result"]
    except Exception as e:
        logger.error(f"Error ingesting document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch")
async def ingest_batch(batch: BatchInput):
    """
    Ingest a batch of documents into the vector database.
    """
    try:
        documents = [{"text": doc.text, "metadata": doc.metadata} for doc in batch.documents]
        
        result = await ingestion_service.process_batch(
            documents=documents,
            collection_name=batch.collection_name
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "Batch processing failed"))
            
        return {"message": f"Successfully processed {len(batch.documents)} documents"}
    except Exception as e:
        logger.error(f"Error ingesting batch: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    collection_name: str = Form(...),
    metadata: str = Form("{}")
):
    """
    Upload a text file and ingest its content into the vector database.
    """
    try:
        # Read file content
        content = await file.read()
        text = content.decode("utf-8")
        
        # Parse metadata
        try:
            metadata_dict = json.loads(metadata)
        except json.JSONDecodeError:
            metadata_dict = {}
        
        # Add file metadata
        metadata_dict["filename"] = file.filename
        metadata_dict["content_type"] = file.content_type
        
        # Process the document
        result = await ingestion_service.process_document(
            text=text,
            metadata=metadata_dict,
            collection_name=collection_name
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
            
        return {"message": f"Successfully processed file: {file.filename}"}
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
