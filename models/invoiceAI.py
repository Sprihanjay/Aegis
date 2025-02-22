import os
import io
import re
from google.cloud import vision
import json

# Set the path to your service account JSON key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/sprihanjay/Programming/Projects/Aegis/Aegis/backend/models/assurant-451704-ea28859565c4.json"

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

def main():
    # Replace with the correct path to your invoice image file
    image_path = 'backend/models/invoiceImages/Plumbing.png'
    
    # Extract text from the invoice image using Google Cloud Vision OCR
    invoice_text = extract_text_from_image(image_path)
    
    # Save the extracted text to a TXT file
    with open('backend/models/extracted_invoice_text.txt', 'w') as txt_file:
        txt_file.write(invoice_text)
    
    print("Extracted invoice text has been saved to 'backend/models/extracted_invoice_text.txt'.")

if __name__ == "__main__":
    main()
