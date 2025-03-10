import os
import io
from google.cloud import vision
import json

# Set the path to your service account JSON key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "models/assurant-451704-ea28859565c4.json"

def extract_text_from_image(image_path):
    """
    Uses Google Cloud Vision to extract text from the given image.
    """
    # Initialize the Vision API client
    client = vision.ImageAnnotatorClient()

    # Read the image file
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    # Prepare the image for OCR
    image = vision.Image(content=content)

    # Perform text detection on the image
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        # The first element contains the full detected text.
        return texts[0].description
    else:
        return ""

def process_invoice_image(image_path):
    """
    Processes the invoice image to extract text and return it in a data structure.
    """
    # Extract text from the invoice image using Google Cloud Vision OCR
    invoice_text = extract_text_from_image(image_path)
    
    # Store the extracted text in a dictionary
    extracted_data = {
        "invoice_text": invoice_text
    }
    
    return extracted_data

# Example usage
# if __name__ == "__main__":
#     image_path = 'models/invoiceImages/Plumbing.png'
#     extracted_data = process_invoice_image(image_path)
#     print(extracted_data)
