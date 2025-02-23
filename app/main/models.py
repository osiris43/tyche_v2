from flask import current_app


# testing something
def get_dynamodb_table():
    print("hello")
    """Retrieve the DynamoDB table object"""
    return current_app.dynamodb.Table("tyche")
