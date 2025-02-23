import imagehash
import argparse
from PIL import Image

# Function to compute perceptual hashes for images
def compute_hashes(image, hash_type):
    # Convert image to grayscale if it's a PIL Image object
    if isinstance(image, Image.Image):
        img = image.convert('L')
    else:
        # Open image using PIL and convert it to grayscale
        img = Image.open(image).convert('L')
    
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

def image_sim(image1, image2, hash_options, print_hashes=False):
    # List of all possible hash types
    hash_types = []
    if hash_options.get('phash') or hash_options.get('all'):
        hash_types.append('phash')
    if hash_options.get('average') or hash_options.get('all'):
        hash_types.append('average')
    if hash_options.get('whash') or hash_options.get('all'):
        hash_types.append('whash')
    if hash_options.get('colormoment') or hash_options.get('all'):
        hash_types.append('colormoment')
    # if hash_options.get('marrhildreth') or hash_options.get('all'):
    #     hash_types.append('marrhildreth')
    # if hash_options.get('radialvariance') or hash_options.get('all'):
    #     hash_types.append('radialvariance')

    # Compute hashes and compare for each selected hash type
    for hash_type in hash_types:
        hash1 = compute_hashes(image1, hash_type)
        hash2 = compute_hashes(image2, hash_type)

        # Compare similarity
        similarity = []
        value = compare_hashes(hash1, hash2)
        similarity.append(value)

        # print(f"{hash_type}: similarity {similarity:.4f}")

        # # Optionally, print the hash values
        # if print_hashes:
        #     print(f"\t{image1} = {hash1}")
        #     print(f"\t{image2} = {hash2}")
        return similarity

if __name__ == "__main__":
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

    hash_options = {
        'all': args.all,
        'phash': args.phash,
        'average': args.average,
        'whash': args.whash,
        'colormoment': args.colormoment,
        'marrhildreth': args.marrhildreth,
        'radialvariance': args.radialvariance
    }

    image_sim(args.image1, args.image2, hash_options, args.print)
