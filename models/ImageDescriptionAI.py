import os
import io
from google.cloud import vision
from vertexai.generative_models import GenerativeModel
import vertexai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the path to your service account JSON key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

def get_image_labels(image_path):
    """
    Reads an image from disk and returns a list of label descriptions detected by the Vision API.
    """
    client = vision.ImageAnnotatorClient()
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    
    response = client.label_detection(image=image)
    labels = response.label_annotations
    # Return only the description for each label
    return [label.description for label in labels]

def generate_contextual_description(labels):
    """
    Generates a contextual description based on the provided labels using a language model.
    """
    # Initialize Vertex AI
    vertexai.init(project="assurant-451704", location="us-central1")

    # Define the prompt for the generative model
    prompt = f"""
    You are an AI specialized in generating contextual descriptions of images.
    Based on the following labels, generate a detailed description of what the image might depict:
    Labels: {', '.join(labels)}
    """

    # Initialize the generative model
    model = GenerativeModel("gemini-1.5-flash-002")

    # Generate the response
    response = model.generate_content([prompt])

    return response.text.strip()

# Example usage:
if __name__ == '__main__':
    image_path = 'backend/models/ClaimImages/Claim1.jpeg'
    ai_labels = get_image_labels(image_path)
    contextual_description = generate_contextual_description(ai_labels)
    print("Contextual Description:", contextual_description)
