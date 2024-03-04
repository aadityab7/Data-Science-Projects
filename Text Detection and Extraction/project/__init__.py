from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename
import psycopg2
import json
import os
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", os.urandom(12))

# Function to insert image details into the database
def insert_image(batch_number, url, text_inside):
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USERNAME'),
        password=os.environ.get('DB_PASSWORD'))

    c = conn.cursor()
    c.execute(
        """
        INSERT INTO images (batch_number, url, text_inside) 
        VALUES (%s, %s, %s)
        """, 
        (batch_number, url, text_inside)
    )
    conn.commit()
    conn.close()

# Function to create a new batch and return its batch number
def create_batch(num_images = 0):
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USERNAME'),
        password=os.environ.get('DB_PASSWORD'))
    
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO batches 
            (created_at, num_images) 
        VALUES (%s, %s)
        RETURNING batch_number
        """, 
        (datetime.now(), num_images)
    )
    batch_number = c.fetchone()[0]  # Fetch the first value of the result tuple
    conn.commit()
    conn.close()
    return batch_number

#index / home page
@app.route('/', methods=('GET', 'POST'))
@app.route('/home', methods=('GET', 'POST'))
def index():
    return render_template('index.html')

@app.route('/upload_images', methods=['POST'])
def upload_images():
    if 'images' not in request.files:
        return jsonify({'error': 'No images uploaded!!'})

    images = request.files.getlist('images')

    if not images:
        return jsonify({'error': 'No Images Uploaded!!'})

    batch_number = create_batch(len(images))
    print(f"Batch Number: {batch_number}")
    uploaded_paths = []

    for image in images:
        # Generate a secure filename and save the image locally
        filename = secure_filename(image.filename)
        upload_folder = 'image_uploads'  
        os.makedirs(upload_folder, exist_ok=True)
        local_path = os.path.join(upload_folder, filename)
        image.save(local_path)
        uploaded_paths.append(local_path)

        # Insert image details into the database
        insert_image(batch_number, local_path, "")  

    return jsonify({'batch_number': batch_number})

@app.route('/extract_text/<int:batch_number>')
def extract_text(batch_number):
    # Your text extraction logic here
    #fetch how many images for this batch has been processed: 
    #if done then redirect to results page
    #if some images remaining start processing them one by one and send the results to user 
    #and update the database as well.

    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USERNAME'),
        password=os.environ.get('DB_PASSWORD'))
    
    c = conn.cursor()

    c.execute(
        """
        SELECT 
            num_images, num_processed
        FROM batches 
        WHERE batch_number = %s
        """, 
        (batch_number,)
    )

    result = c.fetchone()

    conn.close()

    if result:
        print(result)
        num_images, num_processed = result
        print("Num Images:", num_images)
        print("Num Processed:", num_processed)

        if num_images > num_processed:
            #process the remaining images
            return render_template(
                'text_extraction_progress.html', 
                batch_number = batch_number
            )
        else:
            #redirect to the completed page 
            #already processed all the images
            return redirect(url_for('index'))
    else:
        #no such record exists!!
        return redirect(url_for('index'))