# Uses a lightweight Python version
FROM python:3.13-slim

# Names the directory app
WORKDIR /app

# Copy the dependencies
COPY requirements.txt .

# Install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files to /app
COPY . .

# Document port 8000
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]