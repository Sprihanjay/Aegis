import requests
from serpapi import GoogleSearch
from io import BytesIO
from PIL import Image

# Set up your SerpAPI key
SERPAPI_KEY = "your_serpapi_key"  # Replace with your actual API key

def download_first_image(query):
    params = {
        "q": query,
        "tbm": "isch",  # Image search
        "api_key": "d95857c2366579dd2acfacd6b474da667fd70dcfeb05905d14316e1e09826d6e"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    
    if "images_results" in results and results["images_results"]:
        image_url = results["images_results"][0]["original"]
        
        # Download the image
        img_data = requests.get(image_url).content
        img = Image.open(BytesIO(img_data))
        
        # print("Image downloaded successfully.")
        return img
    else:
        # print("No images found.")
        return None

# Example usage
# img = download_first_image("red toyota corolla")
# print(img)
