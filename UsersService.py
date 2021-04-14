import api
from bottle import get, post, error, abort, request, response, HTTPResponse, route , run

import sqlite3

# create new user
# http --verbose POST localhost:5100/users/ UserName="test4" PassWord="123" Email="test4@gmail.com"
# ./bin/PostUser.sh ./share/user.json



@route('/Users/', method='POST')
def createUser(UsersDB):
    user = request.json

    if not user:
        abort(400)

    posted_fields = user.keys()
    required_fields = {'UserName', 'PassWord', 'Email'}

    if not required_fields <= posted_fields:
        abort(400, f'Missing fields: {required_fields - posted_fields}')

    try:
        user['User_id'] = api.execute(UsersDB, '''
           INSERT INTO users(UserName,PassWord,Email)
            VALUES(:UserName, :PassWord, :Email)
            ''', user)
    except sqlite3.IntegrityError as e:
        abort(409, str(e))

    response.status = 201
    response.set_header('Location', f"/users/{user['User_id']}")
    return user

# authenticate user

@route('/auth/', method='POST')
def checkPassword(UsersDB):
    user = request.json
    userpassword = api.query(UsersDB, 'SELECT PassWord FROM users WHERE UserName = ?;' ,[user['username']], one = True);
    if not userpassword:
        abort(404)
    if userpassword['PassWord'] == user['password']:
        return HTTPResponse({'Authentication':True},200)
    return HTTPResponse({'Authentication':False},401)



# user follow
# http --verbose POST localhost:5100/users/test4/add_follow/  FOLLOWING="test1"

@route('/users/<username>/add_follow/', method='POST')
def addFollower(username, UsersDB):
    FOLLOW = request.json
    if not FOLLOW:
      abort(400)

    try:
       follower_id = api.execute(UsersDB, 'select User_id from users where username =?',[username]);
       following_id = api.execute(UsersDB, 'select User_id from users where username =?',[FOLLOW['FOLLOWING']]);
       api.execute(UsersDB, '''
           INSERT INTO FOLLOW(FOLLOWER,FOLLOWING)
            VALUES(?,?)
            ''', [follower_id,following_id])
    except sqlite3.IntegrityError as e:
        abort(409, str(e))

    response.status = 201

    return FOLLOW

# user unfollow
#http --verbose DELETE http://localhost:5100/users/test1/remove_follower/ FOLLOWING=test2

@route('/users/<username>/remove_follower/', method='DELETE')
def removeFollower(username, UsersDB):
    rusername = request.json
    follower_id = api.query(UsersDB, 'select User_id from users where username =?',[username],one= True);
    following_id = api.query(UsersDB, 'select User_id from users where username =?',[rusername['FOLLOWING']],one= True);
        
    # if this user has follow someone yet
    list_followers = api.query(UsersDB, 'SELECT FOLLOWING FROM FOLLOW WHERE FOLLOWER = ?;', [follower_id['User_id']])

    if not  list_followers:
        abort(400)
    for u in list_followers:
        if u['FOLLOWING'] == following_id['User_id']:
            api.execute(UsersDB, '''
         DELETE FROM FOLLOW WHERE FOLLOWER = ? AND FOLLOWING = ?;
            ''', [follower_id['User_id'], following_id['User_id']])
            return HTTPResponse({'Secuess':True},200)
        return abort(404)
