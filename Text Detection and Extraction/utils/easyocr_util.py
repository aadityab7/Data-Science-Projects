#Easy OCR imports
import easyocr

def easy_ocr_extract_text(file_path: str):
    reader = easyocr.Reader(['en'])

    #easy_ocr_result = reader.readtext(file_path)
    easy_ocr_result = reader.readtext(file_path, detail = 0) #only return text

    return easy_ocr_result