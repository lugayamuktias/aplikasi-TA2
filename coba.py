from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np
from werkzeug.utils import secure_filename
from datetime import datetime
import brotli
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import math
from io import BytesIO

app = Flask(__name__)

# Generate a random key and IV
key = get_random_bytes(32)  # 256-bit key
iv = get_random_bytes(16)    # 128-bit IV

# Path to the static folder
static_folder = os.path.join(app.root_path, 'encrypted')

def encrypt_image(input_image_data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(input_image_data, AES.block_size))

    return ciphertext

def decrypt_image(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    return plaintext

# Fungsi untuk mendekompresi gambar menggunakan Brotli
def decompress_image(input_path, output_path):
    with open(input_path, 'rb') as f_in:
        compressed_data = f_in.read()
        decompressed_data = brotli.decompress(compressed_data)

    with open(output_path, 'wb') as f_out:
        f_out.write(decompressed_data)

# Fungsi untuk memampatkan gambar menggunakan Brotli
def compress_image(input_path, output_path):
    with open(input_path, 'rb') as f_in:
        image_data = f_in.read()
        compressed_data = brotli.compress(image_data)

    with open(output_path, 'wb') as f_out:
        f_out.write(compressed_data)

def embed_image(secret_image, cover_image, output_path):
    global original_secret_size

    # Convert both images to RGB mode if one of them is RGBA
    if cover_image.mode == 'RGBA':
        cover_image = cover_image.convert('RGB')
    if secret_image.mode == 'RGBA':
        secret_image = secret_image.convert('RGB')

    # Get dimensions of the cover image
    width, height = cover_image.size

    # Save the original size of the secret image
    original_secret_size = secret_image.size

    # Resize the secret image to fit within the cover image without stretching
    secret_image = secret_image.resize((width, height))

    # Convert images to numpy arrays
    secret_pixels = np.array(secret_image)
    cover_pixels = np.array(cover_image)

    # Embed the secret image into the cover image using LSB with increased bits
    for y in range(height):
        for x in range(width):
            for c in range(3):  # RGB channels
                # Clear the last 3 LSBs of the cover pixel
                cover_pixels[y, x, c] &= ~7
                # Set the last 3 LSBs of the cover pixel to the corresponding bits of the secret image
                cover_pixels[y, x, c] |= (secret_pixels[y, x, c] >> 5) & 7

    # Save the resulting image
    embedded_image = Image.fromarray(cover_pixels)
    embedded_image.save(output_path)

    # Calculate PSNR and MSE
    mse = np.mean((secret_pixels - cover_pixels) ** 2)
    psnr = 20 * math.log10(255.0 / math.sqrt(mse))

    return psnr, mse

# Modifikasi fungsi ekstraksi gambar untuk mengembalikan nilai PSNR dan MSE
def extract_image(stego_image, output_cover_path, output_secret_path):
    # Get dimensions of the stego image
    width, height = stego_image.size
    # Create a new image to store the extracted secret image
    extracted_image = Image.new('RGB', (width, height))
    extracted_pixels = extracted_image.load()
    # Extract the secret image from the stego image using LSB with increased bits
    for y in range(height):
        for x in range(width):
            pixel = [0, 0, 0]
            for c in range(3):  # RGB channels
                # Extract the last 3 bits from the stego image pixel and use them for the extracted image pixel
                pixel[c] = stego_image.getpixel((x, y))[c] & 7  # Mask with 7 to get last 3 bits
            extracted_pixels[x, y] = tuple(int(p * 255 // 7) for p in pixel)  # Scale and convert to integer
    # Save the extracted secret image
    extracted_image.save(output_secret_path)
    # Save the cover image
    cover_image = stego_image.copy()
    cover_image.save(output_cover_path)

    # # Calculate PSNR and MSE
    # secret_pixels = np.array(extracted_image)
    # cover_pixels = np.array(stego_image)
    # mse = np.mean((secret_pixels - cover_pixels) ** 2)
    # psnr = 20 * math.log10(255.0 / math.sqrt(mse))

    # return psnr, mse

def generate_visual_cbc(image_data):
    img = Image.open(BytesIO(image_data))
    visual_cbc_img = img.copy()
    draw = ImageDraw.Draw(visual_cbc_img)

    block_size = 16  # AES block size is 16 bytes
    width, height = img.size
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            draw.rectangle([x, y, x + block_size, y + block_size], outline='black')

    return visual_cbc_img

@app.route('/')
def index():
    return render_template('index.html', action='embed')

@app.route('/embed', methods=['POST'])
def embed():
    if request.method == 'POST':
        try:
            # Ambil file gambar cover dan gambar rahasia dari formulir
            cover_image = request.files['cover_image']
            secret_image = request.files['secret_image']

            # Simpan file di lokasi yang ditentukan
            cover_image_path = 'static/' + secure_filename(cover_image.filename)
            secret_image_path = 'static/' + secure_filename(secret_image.filename)
            cover_image.save(cover_image_path)
            secret_image.save(secret_image_path)

            # Baca gambar rahasia dan dapatkan ukurannya
            secret_image = Image.open(secret_image_path)
            secret_image_size = secret_image.size

            # Dapatkan timestamp saat ini sebagai bagian dari nama file
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

            # Path untuk menyimpan gambar stego yang disisipkan gambar rahasia
            output_path = f'static/embedded_{timestamp}.png'

            # Memanggil fungsi untuk menyembunyikan gambar rahasia
            psnr, mse = embed_image(secret_image, Image.open(cover_image_path), output_path)

            # Mengirimkan nama file gambar yang dihasilkan dan nilai PSNR dan MSE ke template
            return render_template('index.html', action='embed', output_image_name=os.path.basename(output_path), psnr=psnr, mse=mse)

        except Exception as e:
            return f'Error embedding image: {e}'

@app.route('/extract', methods=['POST'])
def extract():
    if request.method == 'POST':
        try:
            # Ambil file gambar stego dari formulir
            stego_image = request.files['stego_image']

            # Simpan file di lokasi yang ditentukan
            stego_image_path = 'static/' + secure_filename(stego_image.filename)
            stego_image.save(stego_image_path)

            # Baca gambar stego
            stego_image = Image.open(stego_image_path)

            # Dapatkan timestamp saat ini sebagai bagian dari nama file
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

            # Path untuk menyimpan gambar rahasia yang diekstraksi
            output_secret_path = f'static/extracted_secret_{timestamp}.png'
            output_cover_path = f'static/extracted_cover_{timestamp}.png'

            # Call extract_image function
            extract_image(stego_image, output_cover_path, output_secret_path)

            # Redirect ke halaman utama setelah selesai
            return render_template('index.html', action='extract', extracted_image_name=os.path.basename(output_secret_path))

        except Exception as e:
            return f'Error extracting image: {e}'

@app.route('/encrypt', methods=['POST'])
def encrypt():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file:
        filename = file.filename
        input_image_data = file.stream.read()
        
        try:
            img = Image.open(BytesIO(input_image_data))
            encrypted_image = encrypt_image(input_image_data, key, iv)
            visual_cbc_image = generate_visual_cbc(encrypted_image)

            # Save visual CBC image as file
            visual_cbc_filename = 'visual_cbc.png'
            visual_cbc_path = 'static/' + visual_cbc_filename
            visual_cbc_image.save(visual_cbc_path)

            return visual_cbc_filename
        except Exception as e:
            return str(e)

@app.route('/decrypt/<filename>')
def decrypt(filename):
    decrypted_filename = 'decrypted_' + filename
    input_image_path = os.path.join(static_folder, filename)
    output_image_path = os.path.join(static_folder, decrypted_filename)
    decrypt_image(input_image_path, output_image_path, key, iv)
    return send_file(output_image_path, as_attachment=True)


@app.route('/show/<filename>')
def show(filename):
    return send_file(os.path.join(static_folder, filename), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)