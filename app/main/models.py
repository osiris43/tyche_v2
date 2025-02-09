from flask import current_app


def get_dynamodb_table():
    """Retrieve the DynamoDB table object"""
    return current_app.dynamodb.Table("OptionsFlow")
