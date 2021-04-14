-- $ sqlite3 users.db < users.sql

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;


DROP TABLE IF EXISTS FOLLOW;
DROP TABLE IF EXISTS users;

CREATE TABLE Users(
    User_id INTEGER primary key NOT NULL,
    UserName VARCHAR NOT NULL,
    PassWord VARCHAR NOT NULL,
    Email VARCHAR NOT NULL, 
    UNIQUE(UserName,Email)

);
INSERT INTO users(UserName,PassWord,Email) VALUES
("test1","123","test1@gmail.com"),
("test2","123","test2@gmail.com"),
("test3","123","test3@gmail.com");


CREATE TABLE FOLLOW (
    F_id INTEGER primary key NOT NULL,
    FOLLOWER INTEGER NOT NULL,
    FOLLOWING INTEGER NOT NULL,

    FOREIGN KEY(FOLLOWER) REFERENCES Users(User_id)
    FOREIGN KEY(FOLLOWING) REFERENCES Users(User_id)
    UNIQUE(FOLLOWER,FOLLOWING)
);
INSERT INTO FOLLOW(FOLLOWER,FOLLOWING) VALUES
(1,3),
(1,2),
(2,3),
(2,1),
(3,1),
(3,2);

COMMIT;
