-- $ sqlite3 timelines.db < timelines.sql

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS POST;


CREATE TABLE POST(
 Post_id INTEGER primary key NOT NULL,
 Text VARCHAR, 
 PostTimeStamp timestamp default CURRENT_TIMESTAMP NOT NULL,
 P_UserId INTEGER NOT NULL

 );

INSERT INTO POST(Text,P_UserId) VALUES 
('This is a test1', 1 ),
('This is a test2', 2 ),
('This is a test3', 3 ),
('This is a test1', 1 ),
('This is a test2', 2 ),
('This is a test3', 3 ),
('This is a test1', 1 ),
('This is a test2', 2 ),
('This is a test3', 3 ),
('This is a test1', 1 ),
('This is a test2', 2 ),
('This is a test3', 3 ),
('This is a test1', 1 ),
('This is a test2', 2 ),
('This is a test3', 3 ),
('This is a test1', 1 ),
('This is a test2', 2 ),
('This is a test3', 3 ),
('This is a test1', 1 ),
('This is a test2', 2 ),
('This is a test3', 3 ),
('This is a test1', 1 ),
('This is a test2', 2 ),
('This is a test3', 3 ),
('This is a test1', 1 ),
('This is a test2', 2 ),
('This is a test3', 3 );
COMMIT;
