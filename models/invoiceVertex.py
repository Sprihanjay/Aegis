import os
import vertexai
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel, Part
import json
from dotenv import load_dotenv

def load_environment_variables():
    load_dotenv()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

def initialize_vertex_ai(project, location):
    vertexai.init(project=project, location=location)

def create_prompt(invoice_text):
    return f"""
    You are a very professional document summarization specialist.
    Please extract the following information from the given document:
    - Net Amount
    - Invoice Description
    - Billing Address
    - Party Name
    - Invoice Date
    - Invoice Number

    Document:
    {invoice_text}
    """

def generate_response(model, prompt):
    return model.generate_content([prompt])

def parse_response(response_text):
    invoice_data = {}
    lines = response_text.split('\n')
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            invoice_data[key.strip()] = value.strip()
    return invoice_data

def process_invoice_with_vertex_ai(invoice_text):
    try:
        # Load environment variables
        load_environment_variables()

        # Initialize Vertex AI
        initialize_vertex_ai(project="assurant-451704", location="us-central1")

        # Create the prompt for the generative model
        prompt = create_prompt(invoice_text)

        # Initialize the generative model
        model = GenerativeModel("gemini-1.5-flash-002")

        # Generate the response
        response = generate_response(model, prompt)

        # Parse the response text to extract the information into a dictionary
        invoice_data = parse_response(response.text)

        return invoice_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# if __name__ == "__main__":
#     print(process_invoice_with_vertex_ai("models/extracted_invoice_text.txt"))
