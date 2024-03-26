import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

unix_socket = os.environ['DB_HOST']

conn = psycopg2.connect(database = os.environ['DB_NAME'],
                        user = os.environ['DB_USERNAME'],
                        password = os.environ['DB_PASSWORD'], 
                        host = unix_socket)

# Open a cursor to perform database operations
cur = conn.cursor()

with open('project/schema.sql') as f:
    sql_commands = f.read()
    cur.execute(sql_commands)

conn.commit()

cur.close()
conn.close()