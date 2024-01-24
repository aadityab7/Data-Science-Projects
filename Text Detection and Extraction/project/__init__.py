from flask import Flask, render_template, request, url_for, flash, redirect, abort, jsonify, session

import json
import os
import requests

import utils

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", os.urandom(12))
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

#index / home page
@app.route('/', methods=('GET', 'POST'))
@app.route('/home', methods=('GET', 'POST'))
def index():
    
    return render_template('ocr.html')
    
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