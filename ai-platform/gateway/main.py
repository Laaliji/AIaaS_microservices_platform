import httpx
from fastapi import FastAPI, Request
import os

app = FastAPI()

TEXT_GEN_SERVICE_URL = os.getenv("TEXT_GEN_SERVICE_URL", "http://text-gen:8000")

@app.get("/health")
def read_root():
    return {"status": "ok"}

@app.get("/generate")
async def generate_proxy(request: Request):
    async with httpx.AsyncClient() as client:
        # Forward the request to the text-gen service
        response = await client.get(f"{TEXT_GEN_SERVICE_URL}/generate", params=request.query_params)
        return response.json()
