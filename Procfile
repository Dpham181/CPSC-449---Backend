gateway: python3 -m bottle --bind=localhost:$PORT --debug --reload gateway
UsersService: python3 -m bottle --bind=localhost:$PORT --debug --reload UsersService
TimelinesService: python3 -m bottle --bind=localhost:$PORT --debug --reload TimelinesService
MessageService: python3 -m bottle --bind=localhost:$PORT --debug --reload MessageService
api: python3 -m bottle --bind=localhost:$PORT --debug --reload api
dynamodb: java -D"java.library.path=./dynamodb_local_latest/DynamoDBLocal_lib" -jar ./dynamodb_local_latest/DynamoDBLocal.jar
Search: python3 -m bottle --bind=localhost:$PORT --debug --reload Search
