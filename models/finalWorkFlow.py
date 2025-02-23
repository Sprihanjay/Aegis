import os
import concurrent.futures
from invoiceAI import process_invoice_image
from invoiceVertex import (
    load_environment_variables,
    initialize_vertex_ai,
    create_prompt,
    generate_response,
    parse_response,
    process_invoice_with_vertex_ai
)

from metaDataAnalysis import is_image_within_timeframe
from real_vs_fake_ai_detection import predict_image_classification_sample
from imageSearch import download_first_image
from imageSimilarity import image_sim 

def invoice_process(image_path, claim_amount, party_name):
    extracted_data = process_invoice_image(image_path)
    invoice_text = extracted_data["invoice_text"]
    invoice_dictionary = process_invoice_with_vertex_ai(invoice_text)
    
    # Check if the party name and claim amount match the expected values
    if invoice_dictionary.get("**Party Name") == f"** {party_name}" and invoice_dictionary.get("**Net Amount") == f"** {claim_amount}":
        print(invoice_dictionary.get("**Party Name"),party_name)
        return True
    return False

def metadata_process(image_path, incident_date):
    if not is_image_within_timeframe(image_path, incident_date):
        return False
    return True

def real_vs_fake_claim(image_path):
    project = os.getenv("PROJECT_PARAMS")
    endpoint_id = os.getenv("ENDPOINT_ID")
    array = predict_image_classification_sample(
        project=project,
        endpoint_id=endpoint_id,
        location="us-central1",
        filename=image_path
    )
    result = [name for name, conf in zip(array['displayNames'], array['confidences']) if conf > 0.6]
    result = result if result else "human"
    return result[0]

def reverse_image_search_similarity(image_path,text_description):
    downloaded_image = download_first_image(text_description)
    hash_options = {'phash': True}
    similarity_results_1 = image_sim(image_path, downloaded_image, hash_options, print_hashes=True)
    hash_options = {'average': True}
    similarity_results_2 = image_sim(downloaded_image, image_path, hash_options, print_hashes=True)
    hash_options = {'whash': True}
    similarity_results_3 = image_sim(downloaded_image, image_path, hash_options, print_hashes=True)
    hash_options = {'colormoment': True}
    similarity_results_4 = image_sim(downloaded_image, image_path, hash_options, print_hashes=True)
    if similarity_results_1 > 0.6 or similarity_results_2 > 0.6 or similarity_results_3 > 0.6 or similarity_results_4 > 0.9:
        return True
    return False
    

if __name__ == "__main__":
   print(reverse_image_search_similarity("models/test/real_test/Toyota.jpg","red toyota corolla"))
    


