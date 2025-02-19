FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements/prod.txt .
RUN pip install --no-cache-dir -r prod.txt

# Final container
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .

# Set environment variables
ENV FLASK_APP=tyche.py
ENV FLASK_ENV=development
ENV DYNAMODB_ENDPOINT=http://localstack:4566

# Expose ports (for both local development and deployment)
EXPOSE 5050 

# Default command to run the app, using an environment variable for port
CMD ["python", "tyche.py"]
