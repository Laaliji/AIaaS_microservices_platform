from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import sys

# Import the worker
from worker import process_rag_query, ingest_document_batch, check_task_status, celery_app

app = FastAPI()

# Define data models
class RAGRequest(BaseModel):
    query: str
    collection_name: str
    n_results: int = 5

class DocumentInput(BaseModel):
    text: str
    metadata: Dict[str, Any] = {}

class BatchInput(BaseModel):
    documents: List[DocumentInput]
    collection_name: str

class TaskStatusRequest(BaseModel):
    task_id: str

@app.get("/health")
def read_health():
    """Health check endpoint"""
    return {"status": "ok"}

@app.post("/async-rag")
async def submit_rag_query(request: RAGRequest):
    """
    Submit a RAG query for asynchronous processing.
    """
    try:
        # Submit the task to Celery
        task = process_rag_query.delay(
            query=request.query,
            collection_name=request.collection_name,
            n_results=request.n_results
        )
        
        return {
            "task_id": task.id,
            "status": "submitted",
            "message": "RAG query submitted for processing"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/async-batch-ingest")
async def submit_batch_ingest(batch: BatchInput):
    """
    Submit a batch of documents for asynchronous ingestion.
    """
    try:
        # Convert documents to the format expected by the task
        documents = [
            {
                "text": doc.text,
                "metadata": doc.metadata
            }
            for doc in batch.documents
        ]
        
        # Submit the task to Celery
        task = ingest_document_batch.delay(
            documents=documents,
            collection_name=batch.collection_name
        )
        
        return {
            "task_id": task.id,
            "status": "submitted",
            "message": f"Batch of {len(batch.documents)} documents submitted for ingestion"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    """
    Check the status of a task.
    """
    try:
        # Submit the task to check status
        task = check_task_status.delay(task_id=task_id)
        result = task.get(timeout=5)  # Wait for up to 5 seconds for the result
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks/active")
async def get_active_tasks():
    """
    Get a list of active tasks.
    """
    try:
        # Get active tasks from Celery
        inspector = celery_app.control.inspect()
        active_tasks = inspector.active()
        
        if not active_tasks:
            return {"active_tasks": []}
        
        # Format the response
        formatted_tasks = []
        for worker, tasks in active_tasks.items():
            for task in tasks:
                formatted_tasks.append({
                    "task_id": task["id"],
                    "name": task["name"],
                    "args": task["args"],
                    "kwargs": task["kwargs"],
                    "worker": worker
                })
        
        return {"active_tasks": formatted_tasks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
