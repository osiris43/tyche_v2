from flask import Flask
from app.main.routes import main_bp
import boto3
import logging
import os


def create_app():
    app = Flask(__name__)

    app.config["DEBUG"] = True
    app.config["ENV"] = "development"  # Optional

    # Set up logging
    logging.basicConfig(level=logging.DEBUG)  # Enable Debug Logging
    app.logger.setLevel(logging.DEBUG)  # Apply debug level to Flask logs

    # Print startup info
    app.logger.debug("Flask app is starting in DEBUG mode.")
    app.logger.debug(f"DynamoDB Endpoint: {os.getenv('DYNAMODB_ENDPOINT')}")
    app.logger.debug(f"AWS Region: {os.getenv('AWS_REGION', 'us-east-2')}")

    # Load Configuration
    app.config.from_object("config.Config")
    print(f"Config Object: {app.config}")

    # Debugging: Print environment variables
    print(f"DynamoDB Endpoint: {os.getenv('DYNAMODB_ENDPOINT')}")
    print(f"AWS Region: {os.getenv('AWS_REGION', 'us-east-2')}")

    # ✅ Initialize DynamoDB connection (Uses Lightsail environment variables)
    app.dynamodb = boto3.resource(
        "dynamodb",
        region_name=os.getenv("AWS_REGION", "us-east-2"),
        endpoint_url=(
            os.getenv("DYNAMODB_ENDPOINT") if os.getenv("DYNAMODB_ENDPOINT") else None
        ),  # None uses AWS
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    # Register Blueprints
    app.register_blueprint(main_bp)

    return app
