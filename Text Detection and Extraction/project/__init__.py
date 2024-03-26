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

from utils import ocr

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", os.urandom(12))
socketio = SocketIO(app)

def get_db_connection(
):
    """
    function to establish connection to the database
    """
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USERNAME'),
        password=os.environ.get('DB_PASSWORD'))

    return conn

# Function to insert image details into the database
def insert_image(batch_id, url):
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute(
        """
        INSERT INTO images (batch_id, url) 
        VALUES (%s, %s)
        """, 
        (batch_id, url)
    )

    conn.commit()
    conn.close()

# Function to create a new batch and return its batch number
def create_batch(num_images = 0):
    conn = get_db_connection()
    c = conn.cursor()

    c.execute(
        """
        INSERT INTO batches 
            (num_images) 
        VALUES (%s)
        RETURNING batch_id
        """, 
        (num_images,)
    )

    batch_id = c.fetchone()[0]  # Fetch the first value of the result tuple
    conn.commit()
    conn.close()

    return batch_id

def process_images(batch_id):  
    conn = get_db_connection()
    c = conn.cursor()

    c.execute(
        """
        SELECT 
            models_list, processed_models_list
        FROM batches 
        WHERE batch_id = %s
        """, 
        (batch_id,)
    )

    result = c.fetchone()

    conn.close()

    if result:
        models_list, processed_models_list = result
    else:
        models_list, processed_models_list = [], []

    num_models = len(models_list)
    num_models_processed = len(processed_models_list)

    while num_models > num_models_processed:
        #use each model to process all the images in a batch
        #process the remaining images
        extraction_status = process_image(batch_id = batch_id, offset = num_processed)
        if extraction_status == 'OK':
            num_processed += 1            
            socketio.emit('image_processed', {'done_num_processed': num_processed}, namespace='/image_processed')
            print("emitted from socketio")
        else:
            break
    
    socketio.emit('image_processing_finished', namespace='/image_processed')  # Emit countdown_finished event

def process_image(batch_id, offset, limit = 1):
    status = 'WAIT'

    conn = get_db_connection()
    c = conn.cursor()

    c.execute(
        """
        SELECT 
            *
        FROM images 
        WHERE batch_id = %s
        ORDER BY image_id
        OFFSET %s LIMIT %s
        """, 
        (batch_id, offset, limit)
    )

    result = c.fetchone()
    
    if result:
        img_id, batch_id, url, _ = result
    else:
        status = 'NO SUCH RECORD!'
        return status 

    #get the names of available models from the database:
    c.execute(
        """
        SELECT 
            model_id, name
        FROM models
        WHERE available = true
        """
    )

    result = c.fetchall()
    if result:
        list_of_models = ocr.list_of_models
    else:
        list_of_models = []

    extracted_texts = []
    for model in list_of_models:
        extracted_text = ocr.extract_text(file_path = url, model_to_use = model)
        extracted_texts.append(extract_text)

    print(extracted_texts)
    
    c.execute(
        """
        UPDATE images 
        SET 
            processed = true
        WHERE 
            image_id = %s 
        """, 
        (extracted_text, img_id)
    )

    conn.commit()

    c.execute("""
        UPDATE batches 
        SET num_processed = num_processed + 1
        WHERE batch_id = %s 
        """,
        (batch_id,)
    )

    conn.commit()

    conn.close()
    
    status = 'OK'
    return status

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

    batch_id = create_batch(len(images))
    uploaded_paths = []

    for image in images:
        # Generate a secure filename and save the image locally
        #later this will be updated to store the files in the cloud
        filename = secure_filename(image.filename)
        upload_folder = 'image_uploads'  
        os.makedirs(upload_folder, exist_ok=True)
        local_path = os.path.join(upload_folder, filename)
        image.save(local_path)
        uploaded_paths.append(local_path)

        # Insert image details into the database
        insert_image(batch_id, local_path)  

    return jsonify({'batch_id': batch_id})

@app.route('/select_models/<int:batch_id>', methods = ['GET', 'POST'])
def select_models(batch_id):
    if request.method == 'GET':
        return render_template('select_models.html')
    else:
        models_list = request.form.get('models_list')
        
        #save this list of models into corresponding batches record
        conn = get_db_connection()
        c = conn.cursor()
        
        c.execute(
            """
            UPDATE batches
            SET models_list = %s
            WHERE batch_id = %s
            """,
            (models_list, batch_id)
        )

        conn.commit()
        c.close()
        conn.close()

        #and then redirect to extract_text page
        return redirect(url_for('extract_text', batch_id = batch_id))

@app.route('/extract_text/<int:batch_id>')
def extract_text(batch_id):
    # Your text extraction logic here
    #fetch how many images for this batch has been processed: 
    #if done then redirect to results page
    #if some images remaining start processing them one by one and send the results to user 
    #and update the database as well.

    conn = get_db_connection()
    
    c = conn.cursor()

    c.execute(
        """
        SELECT 
            cardinality(models_list), cardinality(processed_models_list)
        FROM batches 
        WHERE batch_id = %s
        """, 
        (batch_id,)
    )

    result = c.fetchone()

    conn.close()

    if result:
        num_models, num_models_processed = result
        print(f"Result: {result}, Num Models: {num_models}, Num Models Processed: {num_models_processed}")

        if num_models > num_models_processed:
            return render_template(
                'text_extraction_progress.html', 
                batch_id = batch_id
            )
        else:
            #we will just redirect to the results page.
            return redirect(url_for('index'))
    else:
        #no such record exists!!
        return redirect(url_for('index'))

@socketio.on('connect', namespace='/image_processed')
def connect():
    print('Client connected')
    batch_id = request.args.get('batch_id', type=int)  # Get the batch_id parameter from the connection URL
    img_processing_thread = threading.Thread(target=process_images, args = (batch_id,))
    img_processing_thread.daemon = True
    img_processing_thread.start()

@socketio.on('disconnect', namespace='/image_processed')
def disconnect():
    print('Client disconnected')
