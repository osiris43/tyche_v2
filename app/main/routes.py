from boto3.dynamodb.conditions import Key
from flask import Blueprint, request, jsonify, current_app, render_template
import time

main_bp = Blueprint("main", __name__)


# @main_bp.route("/")
# old to learn from
# def home():
#     table = current_app.dynamodb.Table("tyche")
#     response = table.query(
#         KeyConditionExpression="symbol_pk = symbol",
#         ExpressionAttributeValues={":symbol": f"Symbol#CFLT"},
#     )
#     return render_template("index.html")


@main_bp.route("/")
def home():
    """Basic route to test DynamoDB connectivity"""
    table = current_app.dynamodb.Table("tyche")

    try:
        # Correctly structure the query
        response = table.query(KeyConditionExpression=Key("symbol_pk").eq("SYMBOL#CLF"))

        # Get the items or an empty list if none exist
        items = response.get("Items", [])

    except Exception as e:
        items = []
        print(f"Error querying DynamoDB: {e}")

    return render_template("index.html", data=items)


@main_bp.route("/track", methods=["POST"])
def track_option():
    """Endpoint to track new options flow"""
    data = request.json
    table = current_app.dynamodb.Table("tyche")

    # Extract required fields
    symbol = data.get("underlying_asset", {}).get("ticker", "UNKNOWN")  # e.g., "CFLT"
    expiration_date = data.get("details", {}).get(
        "expiration_date", "UNKNOWN"
    )  # e.g., "2025-04-17"
    contract_ticker = data.get("details", {}).get(
        "ticker", "UNKNOWN"
    )  # e.g., "O:CFLT250417C00040000"
    timestamp = int(time.time())  # Current timestamp in seconds

    # Determine if this is a trade or contract entry
    if "trade_details" in data:  # If trade details exist
        contract_trade_sk = f"TRADE#{timestamp}#{contract_ticker}"
    else:
        contract_trade_sk = f"CONTRACT#{expiration_date}#{contract_ticker}"

    # Prepare item for DynamoDB
    item = {
        "symbol_pk": f"SYMBOL#{symbol}",  # Partition Key
        "contract_trade_sk": contract_trade_sk,  # Sort Key
        "timestamp": timestamp,  # Timestamp for time-based filtering
        **data,  # Include all other data fields
    }

    # Store in DynamoDB
    table.put_item(Item=item)

    return jsonify({"message": "Option tracked", "item": item}), 201


1


# @main_bp.route("/flow/<symbol>", methods=["GET"])
# def get_option_flow(symbol):
#     """Fetch option flow for a given symbol"""
#     table = current_app.dynamodb.Table("tyche")
#     response = table.query(
#         KeyConditionExpression="PK = :symbol",
#         ExpressionAttributeValues={":symbol": f"Symbol#{symbol}"},
#     )
#     return jsonify(response.get("Items", []))
