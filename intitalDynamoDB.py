
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
 table = dynamodb.Table(api.tableName)
 table.delete()

table = dynamodb.create_table(
    TableName='Message',
    KeySchema=[
        {
            'AttributeName': 'messageId',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'TimeStamps',
            'KeyType': 'RANGE'
        },
        
    ],
    LocalSecondaryIndexes = [
    {
    'IndexName' :'Sender',        
    'KeySchema':[
        {
            'AttributeName': 'messageId',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'From',
            'KeyType': 'RANGE'
        }
     ],
     'Projection':{'ProjectionType':'ALL'}         
                
    
    }
    
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'messageId',
            'AttributeType': 'S'
        },
       
        {
            'AttributeName': 'From',
            'AttributeType': 'S'
        },
        
         {
            'AttributeName': 'TimeStamps',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
       'ReadCapacityUnits': 10,
       'WriteCapacityUnits': 10
    }
)

with table.batch_writer() as batch:
        # Conversation of sender:test1 and rec:test2
        # all the reply from test2 will be call in function
	batch.put_item(
	   Item={
		'messageId': '9cbb7fbe-5608-4857-9cf8-4ddb3f4c9869',
		'To': '2',
		'From': '1',
		'message': 'Hi, How are u?',
		'TimeStamps': currentDataTime,
                'quick-replies':['I am fine','Cant talk','Call Me']
	    }

	    
	)
	batch.put_item(
	   Item={
		'messageId': 'aec67e05-9ae6-444f-8cd9-dcf00d738572',
		'To': '2',
		'From': '1',
		'message': 'Hi, How are u?',
		'TimeStamps': currentDataTime,
	    }

	    
	)
	
	# conversation of sender:test3 and rec:test2
	# REGULAR DM
	batch.put_item(
	   Item={
		'messageId': 'd2a05afc-ea97-41ac-a377-189b716138a2',
		'To': '2',
		'From': '3',
		'message':'Where u at?',
		'TimeStamps': currentDataTime

	    }

	    
	)
	batch.put_item(
	   Item={
		'messageId': '5455bd85-e78c-4239-a3a5-1e45900ad3e0',
		'To': '2',
		'From': '3',
		'message': 'Hi, How are u?',
		'TimeStamps': currentDataTime,
                'quick-replies':['I am fine','Cant talk','Call Me']
	    }

	    
	)
	# REPLY TO REGULAR DM
	batch.put_item(
	   Item={
		'messageId': '682f260b-d040-4458-bc3f-393ce131397f',
		'To': '3',
		'From': '2',
		'In-reply-to': 'd2a05afc-ea97-41ac-a377-189b716138a2',
		'message': 'I am at home',
		'TimeStamps': currentDataTime

	    }

	    
	)
	batch.put_item(
	   Item={
		'messageId': '528f8dc7-49b6-4f0d-89a6-80bf203fdaec',
		'To': '3',
		'From': '2',
		'In-reply-to': 'd2a05afc-ea97-41ac-a377-189b716138a2',
		'message': 'I am at store',
		'TimeStamps': currentDataTime

	    }

	    
	)
	batch.put_item(
	   Item={
		'messageId': 'd8cf11a3-3cd2-4099-84c4-b71e65fa30cd',
		'To': '3',
		'From': '2',
		'In-reply-to': 'd2a05afc-ea97-41ac-a377-189b716138a2',
		'message': 'I am at work',
		'TimeStamps': currentDataTime

	    }

	    
	)
	
	



