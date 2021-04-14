
# java -D"java.library.path=./DynamoDBLocal_lib" -jar DynamoDBLocal.jar
# aws dynamodb list-tables --endpoint-url http://localhost:8000


import boto3
import sys
import json
import textwrap
import bottle
from bottle import route, request, response, auth_basic , abort
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime
import api

table = boto3.resource('dynamodb', endpoint_url=api.dynamodbUrl).Table(api.tableName)

app = bottle.default_app()


now = datetime.now()


if not sys.warnoptions:
    import warnings
    warnings.simplefilter('ignore', ResourceWarning)
    
    
def quickcheck(payload):
 list_quickRep = ['call me', 'hi','how are you?','I am busy']
 if payload.__contains__('quickReplies'):
  message = list_quickRep[int(payload['quickReplies'])]
  return message
 return payload['message'] 
 

 # http POST localhost:5000/test1/Message/test2  message="Hi, How are you?" --auth test1:123
@route('/<fromU>/Message/<toU>', method='POST')
def sendDirectMessage(toU, fromU):
 payload = request.json
 message = quickcheck(payload)
 Increment = table.item_count +1 
 currentDataTime = now.strftime("%d/%m/%Y %H:%M:%S")
 rep = table.put_item(
   Item={
        'messageId': str(Increment),
        'from': str(fromU),
        'to': str(toU),
        'message': message,
        'reps':[],
        'Timestamp': currentDataTime
        }  
 )

 return rep


# http PUT localhost:5000/Message/4/reply/ message="I am fine, How about u?"  --auth test1:123
# http PUT localhost:5000/Message/4/reply/ quickReplies=3  --auth test1:123
@route('/Message/<messageid>/reply/', method='PUT')
def replyToDirectMessage(messageid):
 payload = request.json
 message = quickcheck(payload)
 currentDataTime = now.strftime("%d/%m/%Y %H:%M:%S")
 response = table.query(
    KeyConditionExpression=Key('messageId').eq(str(messageid))
 )
 reps = response['Items'][0]['reps']

 reps.append({currentDataTime:message})
 rep = table.update_item(
    Key={
        'messageId': messageid
    },
    UpdateExpression='SET reps = :val1',
    ExpressionAttributeValues={
        ':val1': reps
    }
 )
 return rep
 
 
# http GET localhost:5000/Message/test4 --auth test4:123 

@route('/Message/<username>', method='GET')
def listDirectMessagesFor(username): 
 response = table.scan(
    FilterExpression=Attr('from').eq(username)
 )

 items = response['Items']


 return json.dumps(items[0:])
 
# http GET localhost:5000/Message/1/reply --auth ProfAvery:password
@route('/Message/<messageid>/reply', method='GET')
def listRepliesTo(messageid):
 response = table.query(
    KeyConditionExpression=Key('messageId').eq(str(messageid))
 )
 reps = response['Items'][0]['reps']
 
 return json.dumps(reps[0:])


