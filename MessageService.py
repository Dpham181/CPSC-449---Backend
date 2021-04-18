
# java -D"java.library.path=./DynamoDBLocal_lib" -jar DynamoDBLocal.jar
# aws dynamodb list-tables --endpoint-url http://localhost:8000


import boto3
import botocore
import sys
import json
import bottle
from bottle import route, request, response, auth_basic , abort
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime
import api
import uuid
from decimal import Decimal
table = boto3.resource('dynamodb', endpoint_url=api.dynamodbUrl).Table(api.tableName)

now = datetime.now()
currentDataTime = now.strftime("%d/%m/%Y %H:%M:%S")





        
if not sys.warnoptions:
    import warnings
    warnings.simplefilter('ignore', ResourceWarning)
    
    
def quickcheck(payload,SenderDM):
 if not payload:
  abort(400)
 if 'quick-reply'in payload and 'quick-replies' in SenderDM:
  listquickR= SenderDM['quick-replies']
  return listquickR[int(payload['quick-reply'])]
 return payload['message'] 
 

 # http POST localhost:5000/Message/ From=test1 To=test3  message="Hello, How are you" --auth test1:123
 # http POST localhost:5000/Message/ From=test1 To=test3  message="Hello, are you busy?" quickreplies="Cant talk,Busy Now,Whatsup" --auth test1:123
@route('/Message/', method='POST')
def sendDirectMessage(UsersDB):
 payload = request.json
 if not payload:
  abort(400)
 SendToID= api.query(UsersDB, 'select User_id from users where username =?',[payload['To']], one = True)
 SendFromID= api.query(UsersDB, 'select User_id from users where username =?',[payload['From']], one = True)
 if not SendToID or not SendFromID:
  abort(404)
 DM = {
       'messageId':str(uuid.uuid4()),
	'To': str(SendToID['User_id']),
	'From':str(SendFromID['User_id']),
        'message': payload['message'],
        'TimeStamps': currentDataTime
        }  
 if payload.__contains__('quickreplies'):
  DM['quick-replies'] = payload['quickreplies'].split(",")
 rep = table.put_item(
   Item=DM
 )

 return rep

# http POST localhost:5000/Message/aec67e05-9ae6-444f-8cd9-dcf00d738572/reply/ message="I am good"  --auth test2:123
# http POST localhost:5000/Message/aec67e05-9ae6-444f-8cd9-dcf00d738572/reply/ message="I feel sick"  --auth test2:123
# http POST localhost:5000/Message/aec67e05-9ae6-444f-8cd9-dcf00d738572/reply/ message="I am busy"  --auth test2:123
# http POST localhost:5000/Message/9cbb7fbe-5608-4857-9cf8-4ddb3f4c9869/reply/ quick-reply='0'  --auth test2:123
# http POST localhost:5000/Message/9cbb7fbe-5608-4857-9cf8-4ddb3f4c9869/reply/ quick-reply='1'  --auth test2:123
# http POST localhost:5000/Message/9cbb7fbe-5608-4857-9cf8-4ddb3f4c9869/reply/ quick-reply='2'  --auth test2:123
@route('/Message/<messageid>/reply/', method='POST')
def replyToDirectMessage(messageid):
 response = table.query(
    KeyConditionExpression=Key('messageId').eq(messageid)
 )
 sender = response["Items"]
 if not sender:
  abort(404)
 message = quickcheck(payload,sender[0])
 rep = table.put_item(
   Item={
       'messageId':str(uuid.uuid4()),
       'In-reply-to': sender[0]['messageId'],
	'To': sender[0]['From'],
	'From':sender[0]['To'],
        'message': message,
        'TimeStamps': currentDataTime
        }  
 )


 return  rep
 
  
# http GET localhost:5000/Message/test1 --auth test1:123 

@route('/Message/<username>', method='GET')
def listDirectMessagesFor(username, UsersDB): 
 User= api.query(UsersDB, 'select User_id from users where username =?',[username], one = True)
 if not User:
  abort(404)
 response = table.scan(
    IndexName='Sender',
    FilterExpression=Attr('From').eq(str(User['User_id']))
 )
 items = response['Items']
 return json.dumps(items[0:])
 
# http GET localhost:5000/Message/9cbb7fbe-5608-4857-9cf8-4ddb3f4c9869/reply --auth test1:123

@route('/Message/<messageid>/reply', method='GET')
def listRepliesTo(messageid):
 response = table.scan(
    FilterExpression=Attr('In-reply-to').eq(str(messageid))
 )
 reps = response['Items']
 
 return json.dumps(reps[0:])


