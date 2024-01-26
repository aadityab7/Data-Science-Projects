from flask import Flask, render_template, request, url_for, flash, redirect, abort, jsonify, session
from werkzeug.utils import secure_filename

import json
import os
import requests

from utils import ocr

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", os.urandom(12))
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

#index / home page
@app.route('/', methods=('GET', 'POST'))
@app.route('/home', methods=('GET', 'POST'))
def index():
    
    return render_template('test2.html')
    
    test_files = [
        "./test_images/TEST_0005.jpg", 
        "./test_images/a01-000u-s00-01.png",
        "./test_images/00063690-954d-42e7-86eb-434d9416ead3.jpg"
    ]

    for test_file in ["./test_images/TEST_0005.jpg"]:
        print(f"for the image in {test_file}")
        extracted_texts = utils.extract_text(test_file)
        print(extracted_texts)
        print()

    return "hello"

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
        upload_folder = 'image_uploads'  # You can change this to your preferred folder
        os.makedirs(upload_folder, exist_ok=True)
        local_path = os.path.join(upload_folder, filename)
        image.save(local_path)
        uploaded_paths.append(local_path)

    print(uploaded_paths)
    # Return the local paths of the saved images
    return jsonify({'paths': uploaded_paths})