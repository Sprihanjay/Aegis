import base64

def image_to_base64(image_path):
    """
    Converts an image to base64 encoded image data.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: The base64 encoded image data.
    """
    with open(image_path, "rb") as img_file:
        encoded_image = base64.b64encode(img_file.read()).decode("utf-8")
    return encoded_image

def save_base64_to_file(encoded_image, output_path):
    """
    Saves base64 encoded image data to a file.

    Args:
        encoded_image (str): The base64 encoded image data.
        output_path (str): The path to the output file.
    """
    with open(output_path, "w") as file:
        file.write(encoded_image)

# Example usage
image_path = "models/TestSet/fake_1.jpg"
encoded_image = image_to_base64(image_path)
output_path = "models/TestSet/fake_1_base64.txt"
save_base64_to_file(encoded_image, output_path)
print(f"Base64 encoded image data saved to {output_path}")