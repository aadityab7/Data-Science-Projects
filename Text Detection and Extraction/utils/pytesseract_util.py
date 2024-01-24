#PyTesseract imports
print("importing pyTesseract libs...", end = " ")
import pytesseract
print("done!")

def pytesseract_extract_text(file_path: str):
    #pytesseract_result = pytesseract.image_to_boxes(file_path)
    pytesseract_result = pytesseract.image_to_string(file_path) #return only the text part

    return pytesseract_result