from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime, timedelta

def extract_metadata(image_path):
    img = Image.open(image_path)
    exif_data = img.getexif()
    metadata = {TAGS.get(tag, tag): value for tag, value in exif_data.items()}
    return metadata

def is_image_within_timeframe(image_path, incident_date_str):
    metadata = extract_metadata(image_path)
    
    if 'DateTime' not in metadata:
        print("No DateTime metadata found in the image.")
        return False

    # Convert metadata DateTime and IncidentDate to datetime objects
    image_datetime = datetime.strptime(metadata['DateTime'], "%Y:%m:%d %H:%M:%S")
    incident_date = datetime.strptime(incident_date_str, "%Y-%m-%d")

    # Define the maximum allowed date (incident date + 20 days)
    max_allowed_date = incident_date + timedelta(days=20)

    # Check if image date is within the valid range
    return incident_date < image_datetime <= max_allowed_date

# Example usage
image1 = "metaDataImages/Laptop.JPG"
incident_date = "2025-02-20"  # Example incident date

if is_image_within_timeframe(image1, incident_date):
    print("The image was taken AFTER the incident and within 20 days.")
else:
    print("The image does NOT meet the required timeframe.")
