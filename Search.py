import sys
import json
import bottle
import bottle.ext.redis
import logging.config
from bottle import get, post, error, abort, request, response, HTTPResponse, route , run
import string
import gateway

app = bottle.default_app()
SearchIndex_DB = bottle.ext.redis.RedisPlugin(host='localhost', decode_responses=True)
app.install(SearchIndex_DB)

def checkfields(payload, fields):
 posted_fields = payload.keys()
 required_fields = fields
 if not required_fields <= posted_fields:
  abort(400, f'Missing fields: {required_fields - posted_fields}')
  
def removePunc(word):
 for c in word:
  if c in string.punctuation:
   word = word.replace(c, "")
 return word

def checkTokens(text):
 stop_words = gateway.stop_words.casefold()
 print(stop_words)
 tokens = []
 if text:
  words = text.casefold().split()
  for w in words:
   if not w in stop_words:
    word = removePunc(w)
    tokens.append(word)
 return tokens  
 
 # redis-cli LRANGE is  0 -1 // check 
 # redis-cli flushall 
 # http --verbose http://localhost:5600/index/ postId=1 text='hello, my name is Peter. I am 26 years old!!' 
 # redis-cli --scan | head -10
@route('/index/', method='POST')
def index(rdb):
 payload = request.json
 if not payload:
  abort(400)
 checkfields(payload, {'postId','text'})
 keywords = checkTokens(payload['text'])
 for w in keywords:
  res = rdb.lpush(w, str(payload['postId']))
 if not res:
  abort(404)
 return HTTPResponse(json.dumps(res), 201)
  

 # search 
 # http --verbose http://localhost:5600/search/i
@route('/search/<keyword>', method ='GET')
def search(keyword, rdb):
 if not keyword:
  abort(400)
 res = rdb.lrange(keyword,0,-1)
 if not res:
  abort(404)
 return HTTPResponse(json.dumps(res), 200)
  
#search any keywords list
# http --verbose http://localhost:5600/search-any/ keywords="i,Peter,26" any=1
@route('/search-any/', method='POST')
def any(rdb):
 payload = request.json
 if not payload or not index:
  abort(400)
 listwords = payload['keywords'].casefold().split(',')
 wordsearch = listwords[int(payload['any'])]
 res = {wordsearch:rdb.lrange(wordsearch,0,-1)}
 if not res:
  abort(404)
 return HTTPResponse(res, 200)
 
#search all keywordlist
#http --verbose http://localhost:5600/search-all/ keywords="i,Peter,26"
@route('/search-all/', method='POST')
def all(rdb):
 payload = request.json
 reponseList = []
 if not payload or not index:
  abort(400)
 listwords = payload['keywords'].casefold().split(',')
 for w in listwords:
  reponseList.append({w:rdb.lrange(w,0,-1)})
 if not reponseList:
  abort(404)
 return HTTPResponse(json.dumps(reponseList), 200)

#exclude search
#http --verbose http://localhost:5600/search-exclude/ includeList="i,Peter,26"  excludeList="old,years,26"
@route('/search-exclude/', method='POST')
def exclude(rdb):
 payload = request.json
 reponseList = []
 if not payload:
  abort(400)
 checkfields(payload, {'includeList','excludeList'})
 includelist = payload['includeList'].casefold().split(',')
 excludeList = payload['excludeList'].casefold().split(',')
 words_search = [w for w in includelist if w in excludeList]
 print(words_search)
 for w in words_search:
  reponseList.append({w:rdb.lrange(w,0,-1)})
 if not reponseList:
  abort(404)
 return HTTPResponse(json.dumps(reponseList), 200) 

