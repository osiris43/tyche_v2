`docker-compose up -d` starts localstack and flask app

`curl -X POST "http://127.0.0.1:5050/track" -H "Content-Type: application/json" \
     -d '{"PK": "Symbol#CLF", "SK": "Date#2025-02-07#Strike#14C", "volume": 10000}'`

`http://localhost:5050/flow/{ticker}` 

aws dynamodb list-tables --endpoint-url=http://localhost:4566

aws dynamodb create-table \
    --table-name OptionsFlow \
    --attribute-definitions AttributeName=PK,AttributeType=S AttributeName=SK,AttributeType=S \
    --key-schema AttributeName=PK,KeyType=HASH AttributeName=SK,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST \
    --endpoint-url http://localhost:4566 \
    --region us-east-2