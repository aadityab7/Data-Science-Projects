from PIL import Image

#Meta's Nougat imports - to convert other image formats into pdf files
"""print("importing Meta's Nougat libs...")
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image"""

print("importing Easy OCR lib...", end = " ")
from utils import easyocr_util
print("done!")

print("importing google doc AI lib...", end = " ")
#from utils import google_document_ai_util
print("done!")

print("importing pix2text lib...", end = " ")
#from utils import pix2text_util
print("done!")

print("importing pytesseract lib...", end = " ")
#from utils import pytesseract_util
print("done!")

print("importing keras_ocr lib...", end = " ")
#from utils import keras_ocr_util
print("done!")

print("Done with imports!!")

def extract_text(file_path: str, model_to_use: str = "all"):
    
    extracted_texts = []

    print("Extracting text using Easy OCR:")

    if model_to_use == "all" or model_to_use == "easy_ocr":
        extracted_text = easyocr_util.easy_ocr_extract_text(file_path)
        extracted_texts.append({'model_name' : "easy_ocr", 'extracted_text' : extracted_text})

    print("Result : ", extracted_texts[0])

    return extracted_texts

    print("Extracting text using Google Doc AI:")

    if model_to_use == "all" or model_to_use == "google_document_ai":
        extracted_text = google_document_ai_util.google_doc_ai_extract_text(file_path)
        extracted_texts.append({'model_name' : "google_document_ai", 'extracted_text' : extracted_text})

    print("Result : ", extracted_texts[1])

    print("Extracting text using keras_ocr:")
    if model_to_use == "all" or model_to_use == "keras_ocr":
        extracted_text = keras_ocr_util.keras_ocr_extract_text(file_path)
        extracted_texts.append({'model_name' : "keras_ocr", 'extracted_text' : extracted_text}) 

    print("Result : ", extracted_texts[2])

    print("Extracting text using pix2text:")
    if model_to_use == "all" or model_to_use == "pix2text":
        extracted_text = pix2text_util.pix2text_extract_text(file_path)
        extracted_texts.append({'model_name' : "pix2text", 'extracted_text' : extracted_text})
    print("Result : ", extracted_texts[3])

    print("Extracting text using pytesseract:")
    if model_to_use == "all" or model_to_use == "pytesseract":
        extracted_text = pytesseract_util.pytesseract_extract_text(file_path)
        extracted_texts.append({'model_name' : "pytesseract", 'extracted_text' : extracted_text})
    print("Result : ", extracted_texts[4])

    return extracted_texts

def meta_nougat_extract_text(file_path: str):
    pass