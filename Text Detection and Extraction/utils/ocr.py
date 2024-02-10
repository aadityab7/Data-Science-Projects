from PIL import Image

#Meta's Nougat imports - to convert other image formats into pdf files
"""print("importing Meta's Nougat libs...")
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image"""

print("importing Easy OCR lib...", end = " ")
from utils import easyocr_util
print("done!")

print("importing keras_ocr lib...", end = " ")
from utils import keras_ocr_util
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

print("Done with imports!!")

def extract_text(file_path: str, models_to_use: list = ["all"]):
    extracted_texts = []

    if "all" in models_to_use or "easy_ocr" in models_to_use:
        print("Extracting text using Easy OCR:")
        extracted_text = easyocr_util.easy_ocr_extract_text(file_path)
        extracted_texts.append({'model_name' : "easy_ocr", 'extracted_text' : extracted_text})
        print("Result : ", extracted_texts[-1])

    if "all" in models_to_use or "google_document_ai" in models_to_use:
        print("Extracting text using Google Doc AI:")
        extracted_text = google_document_ai_util.google_doc_ai_extract_text(file_path)
        extracted_texts.append({'model_name' : "google_document_ai", 'extracted_text' : extracted_text})
        print("Result : ", extracted_texts[-1])

    if "all" in models_to_use or "keras_ocr" in models_to_use:
        print("Extracting text using keras_ocr:")
        extracted_text = keras_ocr_util.keras_ocr_extract_text(file_path)
        extracted_texts.append({'model_name' : "keras_ocr", 'extracted_text' : extracted_text}) 
        print("Result : ", extracted_texts[-1])

    if "all" in models_to_use or "pix2text" in models_to_use:
        print("Extracting text using pix2text:")
        extracted_text = pix2text_util.pix2text_extract_text(file_path)
        extracted_texts.append({'model_name' : "pix2text", 'extracted_text' : extracted_text})
        print("Result : ", extracted_texts[-1])

    if "all" in models_to_use or "pytesseract" in models_to_use:
        print("Extracting text using pytesseract:")
        extracted_text = pytesseract_util.pytesseract_extract_text(file_path)
        extracted_texts.append({'model_name' : "pytesseract", 'extracted_text' : extracted_text})
        print("Result : ", extracted_texts[-1])

    return extracted_texts

def meta_nougat_extract_text(file_path: str):
    pass