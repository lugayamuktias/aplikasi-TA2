import io
import os
import sys
from PIL import Image
from Crypto.Cipher import AES
import brotli
import tkinter as tk
from tkinter import filedialog

def pad(data):
    padding_length = AES.block_size - len(data) % AES.block_size
    return data + bytes([padding_length] * padding_length)

def encrypt_image(image_data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(image_data))
    return encrypted_data

def compress_image(image_data):
    return brotli.compress(image_data)

def embed_image(secret_image_data, cover_image, output_path):
    width, height = cover_image.size
    secret_image_size = len(secret_image_data)

    # Resize secret image to match cover image dimensions if necessary
    secret_image = Image.open(io.BytesIO(secret_image_data))
    secret_image = secret_image.resize((width, height), Image.ANTIALIAS)
    secret_image_data = secret_image.tobytes()

    if secret_image_size * 8 > width * height * 3:
        print("Error: Cover image too small to embed secret image.")
        return

    secret_image_data += b'\0' * (width * height * 3 - secret_image_size * 8)

    secret_index = 0
    cover_pixels = cover_image.load()

    for y in range(height):
        for x in range(width):
            r, g, b = cover_pixels[x, y]

            r = r & ~1 | (secret_image_data[secret_index] >> 7)
            g = g & ~1 | (secret_image_data[secret_index + 1] >> 7)
            b = b & ~1 | (secret_image_data[secret_index + 2] >> 7)

            cover_image.putpixel((x, y), (r, g, b))

            secret_index += 3

    cover_image.save(output_path)
    print("Image embedding successful!")

def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
    return file_path

def main():
    # Create GUI window
    root = tk.Tk()
    root.title("Image Steganography")

    # Function to handle encryption and embedding
    def process_images():
        # Step 1: Input secret image
        secret_image_path = upload_image()
        if not secret_image_path:
            return

        # Step 2: Input cover image
        cover_image_path = upload_image()
        if not cover_image_path:
            return

        # Step 3: Encrypt secret image
        key = os.urandom(32)
        iv = os.urandom(16)

        with open(secret_image_path, 'rb') as f:
            secret_image_data = f.read()

        encrypted_secret_image = encrypt_image(secret_image_data, key, iv)

        # Step 4: Compress encrypted image
        compressed_secret_image = compress_image(encrypted_secret_image)

        # Step 5: Embed compressed image into cover image
        cover_image = Image.open(cover_image_path)
        output_path = filedialog.asksaveasfilename(defaultextension=".png")
        if not output_path:
            return

        embed_image(compressed_secret_image, cover_image, output_path)

    # Create a button to trigger the process
    process_button = tk.Button(root, text="Process Images", command=process_images)
    process_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
