FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements/prod.txt .
RUN pip install --no-cache-dir -r prod.txt

COPY . .

# Set environment variables
ENV AWS_ACCESS_KEY_ID=""
ENV AWS_SECRET_ACCESS_KEY=""
ENV FLASK_APP=tyche.py
ENV FLASK_ENV=production
ENV DYNAMODB_ENDPOINT=http://localstack:4566
ENV API_TOKEN=dummy_token

# Expose ports (for both local development and deployment)
EXPOSE 5050
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5050", "tyche:app"]
