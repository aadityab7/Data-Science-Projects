import os
import psycopg2

from dotenv import load_dotenv
load_dotenv()

# Function to initialize the database
def init_db():
    conn = psycopg2.connect(    
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USERNAME'),
        password=os.environ.get('DB_PASSWORD')
    )
    
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS batches (
            batch_number SERIAL PRIMARY KEY, 
            created_at TIMESTAMP, 
            num_images INTEGER DEFAULT 0,
            num_processed INTEGER DEFAULT 0
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id SERIAL PRIMARY KEY, 
            batch_number INTEGER REFERENCES batches(batch_number), 
            url TEXT, 
            text_inside TEXT,
            processed BOOLEAN DEFAULT FALSE
        )
    ''')
    conn.commit()
    conn.close()

init_db()