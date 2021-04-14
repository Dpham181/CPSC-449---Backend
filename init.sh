
sqlite3 ./var/users.db < ./sql/users.sql
sqlite3 ./var/timelines.db < ./sql/timelines.sql
python3 intitalDynamoDB.py
