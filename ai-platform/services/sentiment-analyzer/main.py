from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel

class TextInput(BaseModel):
    text: str

app = FastAPI()

# Load the sentiment analysis model
sentiment_analyzer = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')

@app.post("/analyze")
def analyze_sentiment(data: TextInput):
    # Analyze sentiment using the model
    result = sentiment_analyzer(data.text)
    return result[0]

@app.get("/health")
def read_root():
    return {"status": "ok"}
