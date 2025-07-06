from fastapi import FastAPI
from transformers import pipeline

app = FastAPI()

# Load the text generation model
generator = pipeline('text-generation', model='distilgpt2')

@app.get("/generate")
def generate_text(text: str):
    # Generate text using the model
    result = generator(text, max_length=50, num_return_sequences=1)
    return {"generated_text": result[0]['generated_text']}

@app.get("/health")
def read_root():
    return {"status": "ok"}
