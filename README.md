## Dockerizing and Deploying an ML API to AWS ECS Fargate


The document serves as a comprehensive roadmap for packing a Machine Learning (ML) inference script into a secure container, testing it locally, and shipping it onto a live cloud production pipeline using AWS ECS Fargate.


## Step 1: Building the Application and Dockerfile
Before shipping to the cloud, you need a lightweight application setup and a clean infrastructure blueprint file (Dockerfile).
1. App Setup
Create a project folder named ml-container-app containing the following files:
* requirements.txt (Your app dependencies):textfastapi[standard]==0.115.0
app.py (The core FastAPI engine serving a mock sentiment model):
from fastapi import FastAPI
app = FastAPI()
@app.get(“/”)
def home():
return {“status”: “Machine Learning API is online”}
@app.get(“/predict”)
def predict(text: str):
text_lower = text.lower()
positive_words = [“good”, “great”, “love”, “happy”, “awesome”, “amazing”]
score = sum(1 for word in positive_words if word in text_lower)
sentiment = “Positive” if score > 0 else “Negative”
return {
“input_text”: text,
“sentiment”: sentiment,
“confidence_score”: 0.95 if sentiment == “Positive” else 0.85
}
2. The Docker Blueprint
Create a file named exactly Dockerfile (no extensions) in the same directory:
dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install — no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 8000
CMD [“fastapi”, “run”, “app.py”, “ — port”, “8000”]


### Detailed Deployment steps:
@https://medium.com/@pravashpurkayastha/dockerizing-and-deploying-an-ml-api-to-aws-ecs-fargate-c9b5ba4cdb98
