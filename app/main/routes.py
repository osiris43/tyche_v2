from flask import Blueprint, request, jsonify, current_app, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    table = current_app.dynamodb.Table("OptionsFlow")
    response = table.query(
        KeyConditionExpression="PK = :symbol",
        ExpressionAttributeValues={":symbol": f"Symbol#CLF"},
    )
    return render_template("index.html")


@main_bp.route("/track", methods=["POST"])
def track_option():
    """Endpoint to track new options flow"""
    data = request.json
    table = current_app.dynamodb.Table("OptionsFlow")
    table.put_item(Item=data)
    return jsonify({"message": "Option tracked"}), 201


@main_bp.route("/flow/<symbol>", methods=["GET"])
def get_option_flow(symbol):
    """Fetch option flow for a given symbol"""
    table = current_app.dynamodb.Table("OptionsFlow")
    response = table.query(
        KeyConditionExpression="PK = :symbol",
        ExpressionAttributeValues={":symbol": f"Symbol#{symbol}"},
    )
    return jsonify(response.get("Items", []))
