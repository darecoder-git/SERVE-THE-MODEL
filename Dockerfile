# 1. Start with a lightweight Python blueprint
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the dependencies list into the container
COPY requirements.txt .

# 4. Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your app's code into the container
COPY app.py .

# 6. Expose the port your app runs on
EXPOSE 8000

# 7. Command to run the application when the container starts
CMD ["fastapi", "run", "app.py", "--port", "8000"]
