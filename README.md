`docker-compose up -d` starts localstack and flask app

`curl -X POST "http://127.0.0.1:5050/track" -H "Content-Type: application/json" \
     -d '{"PK": "Symbol#CLF", "SK": "Date#2025-02-07#Strike#14C", "volume": 10000}'`

`http://localhost:5050/flow/{ticker}` 

