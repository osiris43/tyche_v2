# Use official Python base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements/prod.txt 

# Set environment variables
ENV FLASK_APP=tyche.py
ENV FLASK_ENV=development
ENV DYNAMODB_ENDPOINT=http://localstack:4566

# Expose port 5050 for Flask
EXPOSE 5050

# Default command to run the app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5050"]
