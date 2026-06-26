The document serves as a comprehensive roadmap for packing a Machine Learning (ML) inference script into a secure container, testing it locally, and shipping it onto a live cloud production pipeline using AWS ECS Fargate.
Step 1: Building the Application and Dockerfile
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
Step 2: Local Verification (Build & Run)
Open your terminal, navigate to your project directory (cd ml-container-app), and run:
1. Build the Image:bashdocker build -t ml-api .
2. Run the Container Local Testing Environment:bashdocker run -p 8000:8000 ml-api
Become a Medium member
3. Verify: Open your browser and navigate to http://localhost:8000/predict?text=This is awesometo verify the code is running fine inside the environment.
Step 3: Pushing to AWS Elastic Container Registry (ECR) ☁️
AWS Fargate cannot run a container straight from your machine; it must be stored in your AWS infrastructure “warehouse” (ECR).
1. Authenticate your AWS CLI:bashaws configure
2. Create the ECR Repository:bashaws ecr create-repository — repository-name ml-api — region us-east-1
3. Copy the resulting repositoryUri output (referred to below as YOUR_ECR_URI).
4. Log local Docker into AWS ECR:bashaws ecr get-login-password — region us-east-1 | docker login — username AWS — password-stdin YOUR_ECR_URI
5. Tag and Push Image:bashdocker tag ml-api:latest YOUR_ECR_URI:latest
6. bashdocker push YOUR_ECR_URI:latest
Step 4: Configuring AWS Infrastructure via Infrastructure as Code (JSON)
AWS Console layout options change frequently. Using a manual JSON deployment declaration is the most reliable way to register task parameters.
1. Create a file named task-definition.json inside your directory:
json{
“family”: “ml-api-task”,
“containerDefinitions”: [
{
“name”: “ml-api-container”,
“image”: “YOUR_ECR_URI:latest”,
“cpu”: ,
“portMappings”: [
{
“containerPort”: ,
“hostPort”: ,
“protocol”: “tcp”,
“appProtocol”: “http”
}
],
“essential”: true,
“logConfiguration”: {
“logDriver”: “awslogs”,
“options”: {
“awslogs-group”: “/ecs/ml-api-task”,
“awslogs-region”: “us-east-1”,
“awslogs-stream-prefix”: “ecs”,
“awslogs-create-group”: “true”
}
}
}
],
“requiresCompatibilities”: [
“FARGATE”
],
“networkMode”: “awsvpc”,
“cpu”: “256”,
“memory”: “512”,
“executionRoleArn”: “arn:aws:iam::YOUR_12_DIGIT_ACCOUNT_ID:role/ecsTaskExecutionRole”
}
2. Register the Task: Ensure your terminal is matching the location folder path of this JSON and execute:bashaws ecs register-task-definition — cli-input-json file://task-definition.json
Common Errors Faced & How to Fix Them
Error 1: zsh: command not found: docker
Why it happens: The physical engine software application isn’t configured, missing, or installed onto your machine.
The Fix: Download and launch Docker Desktop matching your hardware profile (Intel vs Apple Silicon Mac chips). Restart your terminal session window to apply changes.
Error 2: failed to connect to the docker API… connection refused
Why it happens: The backend core CLI tools are trying to reach out to the core background system daemon engine, but Docker Desktop isn’t actively running.
The Fix: Launch Docker Desktop via your OS application menu panel. Ensure the tray icon whale graphic reaches a stable green/running state before calling shell execution scripts again.
Error 3: Unable to assume the service linked role… (AWSServiceRoleForECS)
Why it happens: Brand new AWS cloud environments run into background race-condition checks when creating an initial ECS cluster from scratch if a background link configuration role doesn’t exist yet.
The Fix: Manually force instant instantiation using the AWS CLI command profile:bashaws iam create-service-linked-role — aws-service-name ://amazonaws.com
Error 4: Fargate requires task definition to have execution role ARN to support log driver awslogs.
Why it happens: AWS Fargate requires precise background execution credentials to pull security images from your private registry and spin up standard logging pipelines (CloudWatch).
The Fix: Save an explicit validation file ecs-trust-policy.json declaring the access schema, generate the role, attach permissions, and paste the ARN pathway explicitly onto your final task definitions sheet:bashaws iam create-role — role-name ecsTaskExecutionRole — assume-role-policy-document file://ecs-trust-policy.json
aws iam attach-role-policy — role-name ecsTaskExecutionRole — policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
Error 5: Unable to load paramfile file://… No such file or directory
Why it happens: Your terminal engine directory pointer path doesn’t align with where the system text file is saved, or literal escape quotation rules contain hidden string spaces.
The Fix: Change directories explicitly directly onto the final target workspace folder (cd /your/exact/path/) and drop absolute text pathways using your window file system drag-and-drop actions.
Final Step: Going Live
1. Navigate to AWS ECS Console ➔ Clusters ➔ Create Cluster (named ml-cluster using Fargate infrastructure logic).
2. Inside ml-cluster, hit Deploy under Services tab. Pick your newly registered ml-api-task, name your service, choose 1 target task runner, and ensure Public IP is set to Enabled.
3. Under your running task execution configuration panel, jump inside the Security Group. Add an Inbound Rule opening up Custom TCP Port 8000 to 0.0.0.0/0 (Anywhere).
4. Retrieve the Public IP from the active Task dashboard window and interact with your model on the web:texthttp://<YOUR_AWS_PUBLIC_IP>:8000/predict?text=Hello world
