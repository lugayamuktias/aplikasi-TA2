from PIL import Image
import brotli
import io

def compress_image(image_path, output_path):
    with open(image_path, 'rb') as f:
        image_data = f.read()

    compressed_data = brotli.compress(image_data)

    with open(output_path, 'wb') as f:
        f.write(compressed_data)

def decompress_image(compressed_path, output_path):
    with open(compressed_path, 'rb') as f:
        compressed_data = f.read()

    decompressed_data = brotli.decompress(compressed_data)

    with open(output_path, 'wb') as f:
        f.write(decompressed_data)
