from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel

class TextInput(BaseModel):
    text: str

app = FastAPI()

# Load the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

@app.post("/generate-embedding")
def generate_embedding(data: TextInput):
    # Generate the embedding
    embedding = model.encode(data.text)
    # Convert numpy array to list for JSON serialization
    return {"embedding": embedding.tolist()}

@app.get("/health")
def read_root():
    return {"status": "ok"}
