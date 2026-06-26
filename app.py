from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Machine Learning API is online"}

@app.get("/predict")
def predict(text: str):
    # A simple deterministic rule acting as our mock ML logic
    text_lower = text.lower()
    positive_words = ["good", "great", "love", "happy", "awesome", "amazing"]
    
    score = sum(1 for word in positive_words if word in text_lower)
    sentiment = "Positive" if score > 0 else "Negative"
    
    return {
        "input_text": text,
        "sentiment": sentiment,
        "confidence_score": 0.95 if sentiment == "Positive" else 0.85
    }
