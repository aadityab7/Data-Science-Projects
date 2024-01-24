#pix2text imports
from pix2text import Pix2Text, merge_line_texts

def pix2text_extract_text(file_path: str):
    p2t = Pix2Text(analyzer_config=dict(model_name='mfd'))

    pix2text_result = p2t.recognize(file_path)
    pix2text_result = merge_line_texts(pix2text_result, auto_line_break=True) #return only the text part

    return pix2text_result