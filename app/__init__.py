from flask import Flask
from app.main.routes import main_bp
import boto3
import os


def create_app():
    app = Flask(__name__)

    # Load Configuration
    app.config.from_object("config.Config")
    print(f"Config Object: {app.config}")

    # Debugging: Print environment variables
    print(f"DynamoDB Endpoint: {os.getenv('DYNAMODB_ENDPOINT')}")
    print(f"AWS Region: {os.getenv('AWS_REGION', 'us-east-2')}")

    # ✅ Fetch AWS Credentials (if using AWS Systems Manager SSM)
    if not os.getenv("AWS_ACCESS_KEY_ID") or not os.getenv("AWS_SECRET_ACCESS_KEY"):
        print("Fetching AWS credentials from SSM...")
        ssm = boto3.client("ssm", region_name=os.getenv("AWS_REGION", "us-east-2"))

        aws_access_key = ssm.get_parameter(
            Name="/lightsail/dynamodb/aws_access_key", WithDecryption=True
        )["Parameter"]["Value"]
        aws_secret_key = ssm.get_parameter(
            Name="/lightsail/dynamodb/aws_secret_key", WithDecryption=True
        )["Parameter"]["Value"]

        os.environ["AWS_ACCESS_KEY_ID"] = aws_access_key
        os.environ["AWS_SECRET_ACCESS_KEY"] = aws_secret_key

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
