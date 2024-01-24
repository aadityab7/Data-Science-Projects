#Google Document API imports
from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # type: ignore

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