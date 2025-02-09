from flask import Flask
from app.main.routes import main_bp
import boto3
import os


def create_app():
    app = Flask(__name__)

    # Load Configuration
    app.config.from_object("config.Config")

    # Initialize DynamoDB connection
    app.dynamodb = boto3.resource(
        "dynamodb",
        region_name="us-east-2",
        endpoint_url=os.getenv("DYNAMODB_ENDPOINT", "http://localhost:4566"),
    )

    # Register Blueprints
    app.register_blueprint(main_bp)

    return app
