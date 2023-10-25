from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # type: ignore

# TODO(developer): Uncomment these variables before running the sample.
project_id = "text-detection-and-extraction"
location = "eu"  # Format is "us" or "eu"
processor_display_name = "text-extraction-document-ocr" # Must be unique per project, e.g.: "My Processor"
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

def quickstart(
    project_id: str,
    processor_id : str,
    location: str,
    file_path: str,
    processor_display_name: str = "text-extraction-document-ocr",
    mime_type: str = "image/jpeg",
):
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


test_image_paths = ["./test_images/TEST_0005.jpg",
                    "./test_images/a01-000u-s00-01.png",
                    "./test_images/00063690-954d-42e7-86eb-434d9416ead3.jpg"]

file_path = test_image_paths[2]
mime_type = extentions_mime_types[file_path.split('.')[-1]]

print(f"project_id, processor_id, location, file_path, processor_display_name, mime_type")
print(project_id, processor_id, location, file_path, processor_display_name, mime_type)
print()

extracted_text = quickstart(project_id, processor_id, location, file_path, processor_display_name, mime_type)
print(f"The document {file_path} contains the following text: {extracted_text}")