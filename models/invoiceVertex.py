import os
import vertexai
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel, Part
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the path to your service account JSON key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Initialize Vertex AI
vertexai.init(project="assurant-451704", location="us-central1")

# Load the extracted invoice text from the file
with open('backend/models/extracted_invoice_text.txt', 'r', encoding='utf-8') as file:
    invoice_text = file.read()

# Define the prompt for the generative model
prompt = f"""
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

# Initialize the generative model
model = GenerativeModel("gemini-1.5-flash-002")

# Generate the response
response = model.generate_content([prompt])

# Parse the response text to extract the information into a dictionary
invoice_data = {}
lines = response.text.split('\n')
for line in lines:
    if ':' in line:
        key, value = line.split(':', 1)
        invoice_data[key.strip()] = value.strip()

# Save the extracted information to a JSON file
with open('backend/models/extracted_invoice_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(invoice_data, json_file, indent=4)

# Print the extracted information
print("Extracted Invoice Data:")
for key, value in invoice_data.items():
    print(f"{key}: {value}")
