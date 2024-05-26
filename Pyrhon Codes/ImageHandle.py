# This functions are for handling images 
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def image_to_bits(image_path):
    # Open the image
    img = Image.open(image_path)
    # Convert image to grayscale
    img = img.convert('L')
    # Convert image to numpy array
    img_array = np.array(img)
    # Flatten the array
    flat_array = img_array.flatten()
    # Convert values to bits
    bits = np.unpackbits(flat_array)
    return bits

def bits_to_image(bits, width, height):
    # Convert bits to integer values
    pixels = np.packbits(bits)
    # Convert to numpy array
    img_array = np.array(pixels).reshape(height, width)
    # Create PIL image from array
    img = Image.fromarray(img_array.astype('uint8'), 'L')
    return img
