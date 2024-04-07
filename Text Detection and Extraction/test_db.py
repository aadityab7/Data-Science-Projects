#test_db.py
import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

def execute_query(query: str, query_type: str = 'fetchone', args = None):
    conn = None
    cursor = None
    
    try:
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST'),
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USERNAME'),
            password=os.environ.get('DB_PASSWORD'),
            sslmode = "require"
        )

        cursor = conn.cursor()

        if args:
            cursor.execute(query, args)
        else:
            cursor.execute(query)
        
        if query_type == 'fetchone':
            result = cursor.fetchone()
        elif query_type == 'fetchall':
            result = cursor.fetchall()
        else:
            result = 'OK'

        conn.commit()

        return result
    except psycopg2.Error as e:
        print("Database error:", e)
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    query = "SELECT * FROM information_schema.tables where table_schema = 'public' and table_type = 'BASE TABLE'"
    result = execute_query(query, query_type = 'fetchall')
    print(f"TABLES: {result}")
    print()
    
    query = "SELECT * FROM batches"
    result = execute_query(query, query_type = "fetchall")
    print(f"data in batches table: {result}")

    query = "SELECT * FROM images"
    result = execute_query(query, query_type = "fetchall")
    print(f"data in images table: {result}")

    query = "SELECT * FROM models"
    result = execute_query(query, query_type = "fetchall")
    print(f"data in models table: {result}")

    query = "SELECT * FROM extracted_texts"
    result = execute_query(query, query_type = "fetchall")
    print(f"data in extracted_texts table: {result}")

    query = "SELECT * FROM batch_model_progress"
    result = execute_query(query, query_type = "fetchall")
    print(f"data in batch_model_progress table: {result}")