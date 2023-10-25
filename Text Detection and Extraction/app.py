from flask import Flask, render_template, request, url_for, flash, redirect, abort, jsonify, session

import json
import os
import requests

#Google Document API Imports
from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # type: ignore

#Easy OCR import
import easyocr

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", os.urandom(12))
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

#index / home page
@app.route('/', methods=('GET', 'POST'))
@app.route('/home', methods=('GET', 'POST'))
def index():
    
    test_files = [
        "./test_images/TEST_0005.jpg", 
        "./test_images/a01-000u-s00-01.png",
        "./test_images/00063690-954d-42e7-86eb-434d9416ead3.jpg"
    ]

    for test_file in test_files:
        print(f"for the image in {test_file}")
        extracted_texts = extract_text(test_file)
        print(extracted_texts)
        print()

    return "hello"

def extract_text(file_path: str, model_to_use: str = "all"):
    
    extracted_texts = []

    if model_to_use == "all" or model_to_use == "google_document_ai":
        extracted_text = google_doc_ai_extract_text(file_path)
        extracted_texts.append({'model_name' : "google_document_ai", 'extracted_text' : extracted_text})

    if model_to_use == "all" or model_to_use == "easy_ocr":
        extracted_text = easy_ocr_extract_text(file_path)
        extracted_texts.append({'model_name' : "easy_ocr", 'extracted_text' : extracted_text})

    return extracted_texts

def easy_ocr_extract_text(file_path: str):
    reader = easyocr.Reader(['en'])

    #easy_ocr_result = reader.readtext(file_path)
    easy_ocr_result = reader.readtext(file_path, detail = 0) #only return text

    return easy_ocr_result

def google_doc_ai_extract_text(file_path: str):
    project_id = "text-detection-and-extraction"
    location = "eu"
    processor_display_name = "text-extraction-document-ocr"
    processor_id = "d208ef269819caba"

    extentions_mime_types = {
        "pdf"   :   "application/pdf",
        "gif"  :   "image/gif",
        "tiff" :   "image/tiff",
        "tif"  :   "image/tiff",
        "jpg"  :   "image/jpeg",
        "jpeg" :   "image/jpeg",
        "png"  :   "image/png",
        "bmp"  :   "image/bmp",
        "webp" :   "image/webp"
    }

    mime_type = extentions_mime_types[file_path.split('.')[-1]]

    # You must set the `api_endpoint`if you use a location other than "us".
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load binary data
    raw_document = documentai.RawDocument(
        content=image_content,
        mime_type=mime_type,  # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
    )

    # Configure the process request
    # `processor.name` is the full resource name of the processor, e.g.:
    # `projects/{project_id}/locations/{location}/processors/{processor_id}`
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)

    # For a full list of `Document` object attributes, reference this page:
    # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
    document = result.document

    #print("retured document :")
    #print(document)

    # Read the text recognition output from the processor
    extracted_text = document.text

    return extracted_text

if __name__ == '__main__':
  app.run(debug = True)