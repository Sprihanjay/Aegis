import imagehash
import argparse
from PIL import Image

# Function to compute perceptual hashes for images
def compute_hashes(image_path, hash_type):
    # Open image using PIL and convert it to grayscale
    img = Image.open(image_path).convert('L')
    
    if hash_type == 'phash':
        return imagehash.phash(img)
    elif hash_type == 'average':
        return imagehash.average_hash(img)
    elif hash_type == 'whash':
        return imagehash.whash(img)
    elif hash_type == 'colormoment':
        return imagehash.colorhash(img)
    elif hash_type == 'marrhildreth':
        return imagehash.marrhildreth(img)
    elif hash_type == 'radialvariance':
        return imagehash.radialvariance(img)
    else:
        raise ValueError(f"Unknown hash type: {hash_type}")

# Function to calculate similarity between two hashes
def compare_hashes(hash1, hash2):
    return 1 - (hash1 - hash2) / len(hash1.hash) ** 2

def main():
    parser = argparse.ArgumentParser(description="Compute and compare perceptual hashes of two images.")
    parser.add_argument("image1", help="Path to the first image.")
    parser.add_argument("image2", help="Path to the second image.")
    parser.add_argument("-all", action="store_true", help="Compute all hashes")
    parser.add_argument("-phash", action="store_true", help="Compute pHash")
    parser.add_argument("-average", action="store_true", help="Compute AverageHash")
    parser.add_argument("-whash", action="store_true", help="Compute WaveletHash")
    parser.add_argument("-colormoment", action="store_true", help="Compute ColorMomentHash")
    parser.add_argument("-marrhildreth", action="store_true", help="Compute MarrHildrethHash")
    parser.add_argument("-radialvariance", action="store_true", help="Compute RadialVarianceHash")
    parser.add_argument("-print", action="store_true", help="Print hash values")

    args = parser.parse_args()

    # Check if at least one hash type is selected
    if not any([args.phash, args.average, args.whash, args.colormoment, args.marrhildreth, args.radialvariance, args.all]):
        print("Error: No hash types selected. Use -all or specific hash options.")
        return

    # List of all possible hash types
    hash_types = []
    if args.phash or args.all:
        hash_types.append('phash')
    if args.average or args.all:
        hash_types.append('average')
    if args.whash or args.all:
        hash_types.append('whash')
    if args.colormoment or args.all:
        hash_types.append('colormoment')
    # if args.marrhildreth or args.all:
    #     hash_types.append('marrhildreth')
    # if args.radialvariance or args.all:
    #     hash_types.append('radialvariance')

    # Load the images
    img1 = Image.open(args.image1)
    img2 = Image.open(args.image2)

    # Compute hashes and compare for each selected hash type
    for hash_type in hash_types:
        hash1 = compute_hashes(args.image1, hash_type)
        hash2 = compute_hashes(args.image2, hash_type)

        # Compare similarity
        similarity = compare_hashes(hash1, hash2)

        print(f"{hash_type}: similarity {similarity:.4f}")

        # Optionally, print the hash values
        if args.print:
            print(f"\t{args.image1} = {hash1}")
            print(f"\t{args.image2} = {hash2}")

if __name__ == "__main__":
    main()
