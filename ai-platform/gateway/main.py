import httpx
from fastapi import FastAPI, Request, Depends, HTTPException, status
import os
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.security import APIKeyHeader

app = FastAPI()

# --- Rate Limiting ---
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- API Key Authentication ---
API_KEY = os.getenv("API_KEY", "default-secret-key")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key: str = Depends(api_key_header)):
    if not api_key or api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
    return api_key

# --- Service URLs ---
TEXT_GEN_SERVICE_URL = os.getenv("TEXT_GEN_SERVICE_URL", "http://text-gen:8000")
SENTIMENT_SERVICE_URL = os.getenv("SENTIMENT_SERVICE_URL", "http://sentiment-analyzer:8000")
EMBEDDINGS_SERVICE_URL = os.getenv("EMBEDDINGS_SERVICE_URL", "http://embeddings-service:8000")
VECTOR_DB_SERVICE_URL = os.getenv("VECTOR_DB_SERVICE_URL", "http://vector-db:8000")
RETRIEVER_SERVICE_URL = os.getenv("RETRIEVER_SERVICE_URL", "http://retriever:8000")
RAG_ORCHESTRATOR_SERVICE_URL = os.getenv("RAG_ORCHESTRATOR_SERVICE_URL", "http://rag-orchestrator:8000")
DATA_INGESTION_SERVICE_URL = os.getenv("DATA_INGESTION_SERVICE_URL", "http://data-ingestion:8000")
ASYNC_PROCESSOR_SERVICE_URL = os.getenv("ASYNC_PROCESSOR_SERVICE_URL", "http://async-processor:8000")

@app.get("/health")
def read_root():
    return {"status": "ok"}

@app.get("/generate", dependencies=[Depends(get_api_key)])
@limiter.limit("5/minute")
async def generate_proxy(request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TEXT_GEN_SERVICE_URL}/generate", params=request.query_params)
        return response.json()

@app.post("/analyze", dependencies=[Depends(get_api_key)])
@limiter.limit("10/minute")
async def sentiment_proxy(request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SENTIMENT_SERVICE_URL}/analyze", json=data)
        return response.json()

@app.post("/generate-embedding", dependencies=[Depends(get_api_key)])
@limiter.limit("10/minute")
async def embeddings_proxy(request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{EMBEDDINGS_SERVICE_URL}/generate-embedding", json=data)
        return response.json()

# Vector DB proxy endpoints
@app.get("/vector-db/collections", dependencies=[Depends(get_api_key)])
@limiter.limit("20/minute")
async def vector_db_list_collections_proxy(request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{VECTOR_DB_SERVICE_URL}/collections")
        return response.json()

@app.post("/vector-db/collections", dependencies=[Depends(get_api_key)])
@limiter.limit("10/minute")
async def vector_db_create_collection_proxy(request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{VECTOR_DB_SERVICE_URL}/collections", json=data)
        return response.json()

@app.get("/vector-db/collections/{collection_name}", dependencies=[Depends(get_api_key)])
@limiter.limit("20/minute")
async def vector_db_get_collection_proxy(collection_name: str, request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{VECTOR_DB_SERVICE_URL}/collections/{collection_name}")
        return response.json()

@app.delete("/vector-db/collections/{collection_name}", dependencies=[Depends(get_api_key)])
@limiter.limit("5/minute")
async def vector_db_delete_collection_proxy(collection_name: str, request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{VECTOR_DB_SERVICE_URL}/collections/{collection_name}")
        return response.json()

@app.post("/vector-db/documents", dependencies=[Depends(get_api_key)])
@limiter.limit("20/minute")
async def vector_db_add_documents_proxy(request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{VECTOR_DB_SERVICE_URL}/documents", json=data)
        return response.json()

@app.post("/vector-db/query", dependencies=[Depends(get_api_key)])
@limiter.limit("30/minute")
async def vector_db_query_proxy(request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{VECTOR_DB_SERVICE_URL}/query", json=data)
        return response.json()

# Retriever proxy endpoints
@app.post("/retrieve", dependencies=[Depends(get_api_key)])
@limiter.limit("30/minute")
async def retriever_proxy(request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{RETRIEVER_SERVICE_URL}/retrieve", json=data)
        return response.json()

@app.get("/retriever/collections", dependencies=[Depends(get_api_key)])
@limiter.limit("20/minute")
async def retriever_list_collections_proxy(request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RETRIEVER_SERVICE_URL}/collections")
        return response.json()

@app.get("/retriever/collections/{collection_name}", dependencies=[Depends(get_api_key)])
@limiter.limit("20/minute")
async def retriever_get_collection_proxy(collection_name: str, request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RETRIEVER_SERVICE_URL}/collections/{collection_name}")
        return response.json()

# RAG Orchestrator proxy endpoints
@app.post("/rag", dependencies=[Depends(get_api_key)])
@limiter.limit("20/minute")
async def rag_proxy(request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{RAG_ORCHESTRATOR_SERVICE_URL}/rag", json=data)
        return response.json()

@app.get("/rag/collections", dependencies=[Depends(get_api_key)])
@limiter.limit("20/minute")
async def rag_list_collections_proxy(request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RAG_ORCHESTRATOR_SERVICE_URL}/collections")
        return response.json()

# Data Ingestion proxy endpoints
@app.post("/ingest", dependencies=[Depends(get_api_key)])
@limiter.limit("20/minute")
async def ingest_document_proxy(request: Request):
    data = await request.json()
    collection_name = request.query_params.get("collection_name")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DATA_INGESTION_SERVICE_URL}/ingest",
            params={"collection_name": collection_name},
            json=data
        )
        return response.json()

@app.post("/batch-ingest", dependencies=[Depends(get_api_key)])
@limiter.limit("10/minute")
async def ingest_batch_proxy(request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{DATA_INGESTION_SERVICE_URL}/batch", json=data)
        return response.json()

@app.post("/upload", dependencies=[Depends(get_api_key)])
@limiter.limit("5/minute")
async def upload_file_proxy(request: Request):
    # This is a multipart form, so we need to forward it as is
    form_data = await request.form()
    
    async with httpx.AsyncClient() as client:
        # Forward the multipart form data
        response = await client.post(
            f"{DATA_INGESTION_SERVICE_URL}/upload",
            files={"file": (form_data["file"].filename, await form_data["file"].read(), form_data["file"].content_type)},
            data={
                "collection_name": form_data["collection_name"],
                "metadata": form_data.get("metadata", "{}")
            }
        )
        return response.json()

# Async Processor proxy endpoints
@app.post("/async-rag", dependencies=[Depends(get_api_key)])
@limiter.limit("30/minute")
async def async_rag_proxy(request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{ASYNC_PROCESSOR_SERVICE_URL}/async-rag", json=data)
        return response.json()

@app.post("/async-batch-ingest", dependencies=[Depends(get_api_key)])
@limiter.limit("10/minute")
async def async_batch_ingest_proxy(request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{ASYNC_PROCESSOR_SERVICE_URL}/async-batch-ingest", json=data)
        return response.json()

@app.get("/task/{task_id}", dependencies=[Depends(get_api_key)])
@limiter.limit("60/minute")
async def task_status_proxy(task_id: str, request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ASYNC_PROCESSOR_SERVICE_URL}/task/{task_id}")
        return response.json()

@app.get("/tasks/active", dependencies=[Depends(get_api_key)])
@limiter.limit("20/minute")
async def active_tasks_proxy(request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ASYNC_PROCESSOR_SERVICE_URL}/tasks/active")
        return response.json()
