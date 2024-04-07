import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

unix_socket = os.environ['DB_HOST']

print("establishing connection with db")
print(f"credentials: host={os.environ.get('DB_HOST')}, database={os.environ.get('DB_NAME')}, user={os.environ.get('DB_USERNAME')}, password={os.environ.get('DB_PASSWORD')}")

conn =  conn = psycopg2.connect(
            host=os.environ.get('DB_HOST'),
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USERNAME'),
            password=os.environ.get('DB_PASSWORD'),
            sslmode = "require"
        )

print("connection established with db")

# Open a cursor to perform database operations
cur = conn.cursor()

with open('project/schema.sql') as f:
    sql_commands = f.read()
    cur.execute(sql_commands)

conn.commit()

cur.close()
conn.close()