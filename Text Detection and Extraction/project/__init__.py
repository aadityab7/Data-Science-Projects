from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename
import psycopg2
import json
import os
from datetime import datetime

from flask_socketio import SocketIO, emit
import random
import time
import threading

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", os.urandom(12))
socketio = SocketIO(app)

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

def process_images(batch_number):
    
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
        num_images, num_processed = result
    else:
        num_images, num_processed = 0, 0

    while num_images > num_processed:
        #process the remaining images
        extraction_status = process_image(batch_number = batch_number, offset = num_processed)
        if extraction_status == 'OK':
            num_processed += 1            
            socketio.emit('image_processed', {'done_num_processed': num_processed}, namespace='/image_processed')
            print("emitted from socketio")
        else:
            break
    
    socketio.emit('image_processing_finished', namespace='/image_processed')  # Emit countdown_finished event

def process_image(batch_number, offset, limit = 1):
    print(f'processing image number: {offset + 1} of batch: {batch_number}')
    status = 'WAIT'

    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USERNAME'),
        password=os.environ.get('DB_PASSWORD'))
    
    c = conn.cursor()

    c.execute(
        """
        SELECT 
            *
        FROM images 
        WHERE batch_number = %s
        ORDER BY id
        OFFSET %s LIMIT %s
        """, 
        (batch_number, offset, limit)
    )

    result = c.fetchone()
    
    if result:
        img_id, batch_number, url, _, _ = result
    else:
        status = 'NO SUCH RECORD!'
        return status 

    print(f"url of the next img to be processed: {url}")

    #use the util methods to actually extract the text here 
    extracted_text = url

    c.execute(
        """
        UPDATE images 
        SET 
            processed = true,
            text_inside = %s
        WHERE 
            id = %s 
        AND 
            batch_number = %s 
        """, 
        (extracted_text, img_id, batch_number)
    )

    conn.commit()

    c.execute("""
        UPDATE batches 
        SET num_processed = num_processed + 1
        WHERE batch_number = %s 
        """,
        (batch_number,)
    )

    conn.commit()

    conn.close()
    
    status = 'OK'
    return status

@socketio.on('connect', namespace='/image_processed')
def connect():
    print('Client connected')
    batch_number = request.args.get('batch_number', type=int)  # Get the batch_number parameter from the connection URL
    
    print(f"making a call to process images for batch: {batch_number}")

    img_processing_thread = threading.Thread(target=process_images, args = (batch_number,))
    img_processing_thread.daemon = True
    img_processing_thread.start()

@socketio.on('disconnect', namespace='/image_processed')
def disconnect():
    print('Client disconnected')

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
        num_images, num_processed = result
        print(f"Result: {result}, Num Images: {num_images}, Num Processed: {num_processed}")

        if num_images > num_processed:
            return render_template(
                'text_extraction_progress.html', 
                batch_number = batch_number
            )
        else:
            #we will just redirect to the results page.
            return redirect(url_for('index'))
    else:
        #no such record exists!!
        return redirect(url_for('index'))