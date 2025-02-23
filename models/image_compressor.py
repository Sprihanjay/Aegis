from PIL import Image
import os

def compress_image(input_path, output_path, target_size_mb=1.4):
    target_size = target_size_mb * 1024 * 1024  # Convert MB to bytes
    img = Image.open(input_path)
    
    # Start with the original image size and quality
    quality = 95
    step = 2  # Reduce quality in small steps
    width, height = img.size

    while True:
        # Save image with current quality setting
        img.save(output_path, "JPEG", quality=quality)
        file_size = os.path.getsize(output_path)

        # Stop if file is just under the target size
        if file_size <= target_size:
            break

        # If reducing quality alone isn't enough, start resizing
        if quality <= 20:
            width = int(width * 0.95)
            height = int(height * 0.95)
            img = img.resize((width, height), Image.LANCZOS)
        
        # Decrease quality slightly
        quality -= step
    
    print(f"Final file size: {file_size / (1024 * 1024):.2f} MB")

# Example usage:
# compress_image("models/TestSet/Image2.jpg", "compressed.jpg")
