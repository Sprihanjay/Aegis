import requests
from serpapi import GoogleSearch

# Set up your SerpAPI key
SERPAPI_KEY = "your_serpapi_key"  # Replace with your actual API key

def download_first_image(query, save_path="image.jpg"):
    params = {
        "q": query,
        "tbm": "isch",  # Image search
        "api_key": "d95857c2366579dd2acfacd6b474da667fd70dcfeb05905d14316e1e09826d6e"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    
    if "images_results" in results and results["images_results"]:
        image_url = results["images_results"][0]["original"]
        
        # Download and save the image
        img_data = requests.get(image_url).content
        with open(save_path, "wb") as handler:
            handler.write(img_data)
        
        print(f"Image downloaded successfully: {save_path}")
    else:
        print("No images found.")

# Example usage
download_first_image("red toyota corolla")
