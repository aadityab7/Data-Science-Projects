#does import time vary depending upon the drive? Nope

print("Starting Imports")

#Easy OCR imports - should take approx. 15 seconds to import
print("Easy OCR Imports")
import easyocr
print("Easy OCR Imports done!")

"""
#keras_ocr imports ~ 9 minutes to import
print("Keras OCR Imports")
import matplotlib.pyplot as plt
import keras_ocr
print("Keras OCR Imports done!")
"""

"""
#pix2text imports ~ 2.6 minutes
print("Pix2Text Imports")
from pix2text import Pix2Text, merge_line_texts
print("Pix2Text Imports done!")
"""

#PyTesseract imports ~ 5 seconds
print("PyTesseract Imports")
import pytesseract
print("PyTesseract Imports done!")

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

"""
#Google Document API imports ~ 30 seconds
print("Google Docs Imports")
from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # type: ignore
print("Google Docs Imports done!")

#Meta's Nougat imports - to convert other image formats into pdf files ~ 4 seconds
print("Meta's Nougat Imports")
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
import subprocess
print("Meta's Nougat Imports done!")
"""

print("Done with imports!!")

def easy_ocr_extract_text(file_path: str):
    reader = easyocr.Reader(['en'])

    #easy_ocr_result = reader.readtext(file_path)
    easy_ocr_result = reader.readtext(file_path, detail = 0) #only return text

    return easy_ocr_result

"""def keras_ocr_extract_text(file_path: str):
    # keras-ocr will automatically download pretrained
    # weights for the detector and recognizer.
    pipeline = keras_ocr.pipeline.Pipeline()
    
    image = [keras_ocr.tools.read(file_path)]

    text_predictions = pipeline.recognize(image)

    #return only the text for now - so extract text from the result
    keras_ocr_result = []
    for prediction in text_predictions[0]:
        keras_ocr_result.append(prediction[0])

    return keras_ocr_result
"""
"""def pix2text_extract_text(file_path: str):
    p2t = Pix2Text(analyzer_config=dict(model_name='mfd'))

    pix2text_result = p2t.recognize(file_path)
    pix2text_result = merge_line_texts(pix2text_result, auto_line_break=True) #return only the text part

    return pix2text_result"""

def pytesseract_extract_text(file_path: str):
    #pytesseract_result = pytesseract.image_to_boxes(file_path)
    pytesseract_result = pytesseract.image_to_string(file_path) #return only the text part

    return pytesseract_result

"""
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

def meta_nougat_extract_text(file_path: str):
    command = "nougat url -o ."
    subprocess.run(command, shell=True)

    return file_path 
"""

list_of_models = [
    "easy_ocr", 
    #"keras_ocr",
    #"pix2text",
    "pytesseract",
    #"google_document_ai",
    #"meta_nougat"
]

def extract_text(file_path: str, model_to_use: str = ""):
    print(f"Extracting text for file: {file_path} using model: {model_to_use}")

    extracted_text = ""

    if model_to_use == "easy_ocr":
        extracted_text = easy_ocr_extract_text(file_path)
    elif model_to_use == "keras_ocr":
        pass
        # extracted_text = keras_ocr_extract_text(file_path)
    elif model_to_use ==  "pix2text":
        pass
        #extracted_text = pix2text_extract_text(file_path)
    elif model_to_use == "pytesseract":
        extracted_text = pytesseract_extract_text(file_path)
    elif model_to_use == "google_document_ai":
        pass
        # extracted_text = google_doc_ai_extract_text(file_path)
    elif model_to_use == "meta_nougat":
        pass
        # extracted_text = meta_nougat_extract_text(file_path)

    print("Result : ", extracted_text)

    return extracted_text