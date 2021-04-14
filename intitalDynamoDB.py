
# java -D"java.library.path=./DynamoDBLocal_lib" -jar DynamoDBLocal.jar
# aws dynamodb list-tables --endpoint-url http://localhost:8000
# aws dynamodb delete-table --table-name Message --endpoint-url http://localhost:8000



import boto3
import api 
from datetime import datetime
now = datetime.now()
currentDataTime = now.strftime("%d/%m/%Y %H:%M:%S")
dynamodb = boto3.resource('dynamodb', endpoint_url=api.dynamodbUrl)

# list all the exits table at localhost port 8000
existing_tables = dynamodb.tables.all() 

# if table exit then del for creating new table
if 'Message' in [t.name for t in existing_tables]:
 table = dynamodb.Table(api.table)
 table.delete()

table = dynamodb.create_table(
    TableName='Message',
    KeySchema=[
        {
            'AttributeName': 'messageId',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'messageId',
            'AttributeType': 'S'
        }
        
    ],
    ProvisionedThroughput={
       'ReadCapacityUnits': 5,
       'WriteCapacityUnits': 5
    }
)
with table.batch_writer() as batch:

	batch.put_item(
	   Item={
		'messageId': '1',
		'from': 'test1',
		'to': 'test2',
		'message': 'this is a message from test1 to test2.',
		'reps':[],
		'Timestamp': currentDataTime

	    }
	    
	)
	batch.put_item(
	   Item={
		'messageId': '2',
		'from': 'test1',
		'to': 'test3',
		'message': 'this is a message from test1 to test3.',
		'reps':[],
		'Timestamp': currentDataTime

	    }
	    
	)
	batch.put_item(
	   Item={
		'messageId': '3',
		'from': 'test2',
		'to': 'test1',
		'message': 'this is a message from test2 to test1.',
		'reps':[],
		'Timestamp': currentDataTime

	    }
	    
	)
	



