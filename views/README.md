# CPSC 449 - Web Back-End Engineering 
# Project 5 
# Spring 2021 due Apr 23 (Section 02)


## We plan to build a microblogging service similar to Twitter
  - Each user has a user timeline consisting of the posts that they have made.
  - Each user has a home timeline consisting of recent posts by all users that this user follows.
  - There is a public timeline consisting of all posts from all users.
  - Timelines are organized in reverse chronological order. When timelines are retrieved through the web service, they should be limited to 25.
  - Introducing an API gateway to mediate between users and our services
  - Adding polyglot persistence by introducing a new microservice built with DynamoDB Local, a version of Amazon’s DynamoDB service that runs locally on your own computer.

# URI host:
1.  http://localhost:5000/ (Gateway)
2.  http://localhost:5100/ (Users service)
3.  http://localhost:5200/ (Timelines service)
4.  http://localhost:5300/ (DM service)
5.  http://localhost:5400/ (api initial splite)

# Files Submission:

**Etc files:**
*`api.ini, `*
*`gateway.ini`*


**view:**
*`home.html`* 

**sql:**
*`users.sql,`* 
*`timelines.sql`* 

**sqlite and dynamodb setup:**
*`api.py,`* 
*`intitalDynamoDB.py`* 

**services:**
*`gateway.py, `* 
*`UsersService.py, `* 
*`MessageService.py, `* 
*`TimelinesService.py`* 

**Profile:**
*`Profile`*  


# Reason of change:
 - In this project 5, I fixed all the error from project 2 by spreading db file into two db. 
 - Added gateway
 - Fixed all the route uri from users and timelines that use to  match with three projects combine. 
 - Redesgined ddl for using Id instead of username.
 - Added view using template for populating the Api call same as README.md.
 - Updated Profile
 - createUser now public in gateway 

# Project exe commandline:

**Database setup commands**

> ```shell-session
> $ ./init.sh 
> ```

> ```shell-session
> $ cd dynamodb_local_latest
> ```

> ```shell-session
> $ java -D"java.library.path=./DynamoDBLocal_lib" -jar DynamoDBLocal.jar
> ```

> ```shell-session
> $ python3 intitalDynamoDB.py 
> ```

**Foreman commands**

*Runinng all the services then open new terminal for Httpie Api call*

> ```shell-session
> $ foreman start 
> ```


# Api calls:

### All the api calls through gateway at port 5000: 

**`createUser(username, email, password)`**

> ```shell-session
> $ http --verbose POST localhost:5000/SignUp/ UserName="test4" PassWord="123" Email="test4@gmail.com" 
> ```

**`checkPassword(username, password)`**

> ```shell-session
> $ http POST localhost:5000/auth/ username=test4 password=123 --auth test4:123
> ```

**`addFollower(username,usernameToFollow)`**

> ```shell-session
> $ http --verbose POST localhost:5000/users/test4/add_follow/  FOLLOWING="test1" --auth test4:123
> ```

**`removeFollower(username, usernameToRemove)`**

> ```shell-session
> $ http --verbose DELETE http://localhost:5000/users/test1/remove_follower/ FOLLOWING=test2 --auth test1:123
> ```

**`getUserTimeline(username)`**

> ```shell-session
> $ http --verbose http://localhost:5000/Posts/test1 --auth test1:123
> ```

**`getPublicTimeline()`**

> ```shell-session
> $ http --verbose http://localhost:5000/Posts --auth test1:123
> ```

**`getHomeTimeline(username)`**

> ```shell-session
> $ http --verbose http://localhost:5000/Posts/home/test2 --auth test2:123
> ```

**`postTweet(username, text)`**

> ```shell-session
> $ http --verbose POST localhost:5000/Posts/ username=test1 Text=test --auth test1:123
> ```

**`sendDirectMessage(to, from, message, quickReplies=None)`**

> ```shell-session
> $ http POST localhost:5000/test3/Message/test1  message="Hi, How are you?" --auth test3:123
> ```

**`replyToDirectMessage(messageId, message)`**

> ```shell-session
> $ http PUT localhost:5000/Message/4/reply/ message="I am fine, How about u?"  --auth test1:123
> ```

> ```shell-session
> $ http PUT localhost:5000/Message/4/reply/ quickReplies=3  --auth test1:123
> ```

**`listDirectMessagesFor(username)`**

> ```shell-session
> $ http GET localhost:5000/Message/test3 --auth test4:123 
> ```

**`listRepliesTo(messageId)`**

> ```shell-session
> $ http GET localhost:5000/Message/4/reply --auth test4:123
> ```

