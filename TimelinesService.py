import api
import sqlite3
from bottle import get, post, error, abort, request, response, HTTPResponse, route , run


# Routes


# get user timelines
# http --verbose http://localhost:5200/Posts/<username>


@route('/Posts/<username>', method='GET')
def getUserTimeline(username,TimeLinesDB,UsersDB):
    UserID= api.query(UsersDB, 'select User_id from users where username =?',[username],one= True);
    userposts = api.query(TimeLinesDB, 'Select POST.TEXT, POST.PostTimeStamp from POST where POST.P_UserId =? Order By Post_id DESC limit 25;', [UserID['User_id']])
    if not userposts:
        abort(404)
    rep = {'POSTS': userposts}
    if len(rep['POSTS']) < 0:
        abort(404)
    return HTTPResponse(rep,200)

# get public timelines
# http --verbose http://localhost:5200/Posts

@route('/Posts', method='GET')
def getPublicTimeline(TimeLinesDB):
    userposts = api.query(TimeLinesDB, 'Select Post_id ,POST.P_UserId,POST.TEXT, POST.PostTimeStamp from POST Order By Post_id DESC limit 25;')
    if not userposts:
        abort(400)
    rep = {'POSTS': userposts}
    if len(rep['POSTS']) < 0:
        abort(404)
    return HTTPResponse(rep,200)


# get Home timelines
# http --verbose http://localhost:5200/Posts/home/<username>

@route('/Posts/home/<username>', method='GET')
def getHomeTimeline(username,TimeLinesDB,UsersDB):

    listoffriends_ID = api.query(UsersDB, 'select following from follow left join users where follow.follower = users.User_id and users.username = ?', [username])
    # if no follower 
    if not listoffriends_ID:
     abort(400)
    list_followingPosts = []
    for f in listoffriends_ID:
     posts = api.query(TimeLinesDB, 'Select POST.P_UserId, POST.TEXT, POST.PostTimeStamp from POST where P_UserId =? Order By Post_id DESC limit 25;', [f['FOLLOWING']])
     for post  in posts:
      userName = api.query(UsersDB, 'select username from users where User_id = ?;',[post['P_UserId']] )
      for usern in userName:
       del post['P_UserId']    
       post['UserName'] = usern['UserName'] 
       list_followingPosts.append(post)


    if not  list_followingPosts:
        abort(400)
        
    rep = {'POSTS': list_followingPosts}
    if len(rep['POSTS']) < 0:
        abort(404)
    return HTTPResponse(rep,200)


#POST Tweet
# http --verbose POST localhost:5200/Posts/ username=test1 Text=test


@route('/Posts/', method='POST')
def postTweet(UsersDB,TimeLinesDB):
    payload = request.json
    UserID= api.query(UsersDB, 'select User_id from users where username =?',[payload['username']], one = True)
    if not payload:
        abort(400)
    try:
        payload['Post_id'] = api.execute(TimeLinesDB, '''
           INSERT INTO POST(Text,P_UserId)
            VALUES(?, ?)
            ''', [payload['Text'],UserID['User_id']])
    except sqlite3.IntegrityError as e:
        abort(409, str(e))
    postcreated = api.query (TimeLinesDB, 'SELECT POST.TEXT, POST.PostTimeStamp from POST WHERE POST.Post_id = ? ',[payload['Post_id']], one =True)

    return HTTPResponse(postcreated,201)
