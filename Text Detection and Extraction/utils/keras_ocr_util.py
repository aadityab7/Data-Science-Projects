#keras_ocr imports
import matplotlib.pyplot as plt

import keras_ocr

def keras_ocr_extract_text(file_path: str):
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