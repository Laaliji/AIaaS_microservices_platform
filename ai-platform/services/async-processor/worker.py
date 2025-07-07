import os
import httpx
import logging
import json
from celery import Celery
from typing import Dict, Any, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ai_platform.async_processor")

# Initialize Celery
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery_app = Celery('tasks', broker=REDIS_URL, backend=REDIS_URL)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Service URLs
RAG_ORCHESTRATOR_URL = os.getenv("RAG_ORCHESTRATOR_SERVICE_URL", "http://rag-orchestrator:8000")
DATA_INGESTION_URL = os.getenv("DATA_INGESTION_SERVICE_URL", "http://data-ingestion:8000")

@celery_app.task(name="process_rag_query", bind=True)
def process_rag_query(self, query: str, collection_name: str, n_results: int = 5) -> Dict[str, Any]:
    """
    Process a RAG query asynchronously.
    
    Args:
        query: The query text
        collection_name: The name of the collection to query
        n_results: Number of results to return
        
    Returns:
        Result of the RAG query
    """
    try:
        logger.info(f"Processing RAG query: {query}")
        
        # Call the RAG orchestrator service
        with httpx.Client() as client:
            response = client.post(
                f"{RAG_ORCHESTRATOR_URL}/rag",
                json={
                    "query": query,
                    "collection_name": collection_name,
                    "n_results": n_results
                }
            )
            
            if response.status_code != 200:
                logger.error(f"Error processing RAG query: {response.text}")
                return {"success": False, "error": response.text}
            
            result = response.json()
            logger.info(f"RAG query processed successfully")
            return {"success": True, "result": result}
            
    except Exception as e:
        logger.error(f"Error processing RAG query: {str(e)}")
        return {"success": False, "error": str(e)}

@celery_app.task(name="ingest_document_batch", bind=True)
def ingest_document_batch(self, documents: List[Dict[str, Any]], collection_name: str) -> Dict[str, Any]:
    """
    Ingest a batch of documents asynchronously.
    
    Args:
        documents: List of documents with text and metadata
        collection_name: Name of the collection to add the documents to
        
    Returns:
        Result of the batch ingestion
    """
    try:
        logger.info(f"Ingesting batch of {len(documents)} documents")
        
        # Call the data ingestion service
        with httpx.Client() as client:
            response = client.post(
                f"{DATA_INGESTION_URL}/batch",
                json={
                    "documents": documents,
                    "collection_name": collection_name
                }
            )
            
            if response.status_code != 200:
                logger.error(f"Error ingesting documents: {response.text}")
                return {"success": False, "error": response.text}
            
            result = response.json()
            logger.info(f"Document batch ingested successfully")
            return {"success": True, "result": result}
            
    except Exception as e:
        logger.error(f"Error ingesting documents: {str(e)}")
        return {"success": False, "error": str(e)}

@celery_app.task(name="check_task_status", bind=True)
def check_task_status(self, task_id: str) -> Dict[str, Any]:
    """
    Check the status of a task.
    
    Args:
        task_id: The ID of the task to check
        
    Returns:
        Status of the task
    """
    try:
        # Get the task result from Celery
        task = celery_app.AsyncResult(task_id)
        
        if task.state == 'PENDING':
            return {
                "task_id": task_id,
                "status": "pending",
                "result": None
            }
        elif task.state == 'FAILURE':
            return {
                "task_id": task_id,
                "status": "failed",
                "result": str(task.result)
            }
        else:
            return {
                "task_id": task_id,
                "status": "completed",
                "result": task.result
            }
            
    except Exception as e:
        logger.error(f"Error checking task status: {str(e)}")
        return {
            "task_id": task_id,
            "status": "error",
            "result": str(e)
        }
