#keras_ocr imports
import keras_ocr

def keras_ocr_extract_text(file_path: str):
    # keras-ocr will automatically download pretrained
    # weights for the detector and recognizer.
    pipeline = keras_ocr.pipeline.Pipeline()
    
    image = keras_ocr.tools.read(file_path) #maybe we need to store this as a list??

    keras_ocr_result = pipeline.recognize(image)

    return keras_ocr_result