from flask import Flask, render_template, request, url_for, flash, redirect, abort, jsonify, session
from werkzeug.utils import secure_filename

import json
import os
import requests

#from utils import ocr

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", os.urandom(12))
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

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

    uploaded_paths = []

    for image in images:
        # Generate a secure filename and save the image locally
        filename = secure_filename(image.filename)
        upload_folder = 'image_uploads'  
        os.makedirs(upload_folder, exist_ok=True)
        local_path = os.path.join(upload_folder, filename)
        image.save(local_path)
        uploaded_paths.append(local_path)

    print('paths', uploaded_paths)
    # Return the local paths of the saved images
    return jsonify({'paths': uploaded_paths})

@app.route('/text_extraction_progress'x)
def text_extraction_progress():
    uploaded_paths = request.form.get('uploaded_paths')

    return render_template(
        'text_extraction_progress.html', 
        uploaded_paths = uploaded_paths
    )

@app.route('/extract_text', methods=['POST'])
def extract_text():
    uploaded_paths = request.form.get('uploaded_paths')

    #make predictions using the uploaded images
    extracted_texts = []
    for path in uploaded_paths:
        extracted_texts.append(ocr.extract_text(path, models_to_use = ["easy_ocr", "keras_ocr"]))

    print('extracted_texts', extracted_texts)

    return jsonify({'extracted_texts' : extracted_texts})