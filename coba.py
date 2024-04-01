from flask import Flask, session, request, render_template, request, redirect, url_for, send_from_directory, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
import os
import io
import numpy as np
from werkzeug.utils import secure_filename
from datetime import datetime
import brotli
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import math
from io import BytesIO

app = Flask(__name__, static_folder='static')

# Fungsi untuk enkripsi AES-CBC
def encrypt_AES_CBC(plaintext, key):
    iv = get_random_bytes(16)  # Inisialisasi vektor inisialisasi
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    return iv, ciphertext

# Fungsi untuk membaca gambar dari file
def read_image(filename):
    with open(filename, 'rb') as f:
        return f.read()

# Fungsi untuk menulis gambar ke file
def write_image(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)

# Fungsi untuk melakukan enkripsi pada gambar
def encrypt_image(image_data, key):
    # Enkripsi data gambar
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Padding data gambar agar ukurannya menjadi kelipatan block size AES
    padded_data = pad(image_data, AES.block_size)
    # Melakukan enkripsi
    ciphertext = cipher.encrypt(padded_data)
    return iv + ciphertext

# Fungsi untuk dekripsi AES-CBC
def decrypt_AES_CBC(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(ciphertext)
    return unpad(decrypted_data, AES.block_size)

# Fungsi untuk membaca gambar terenkripsi dari file
def read_encrypted_image(filename):
    with open(filename, 'rb') as f:
        return f.read()

# Fungsi untuk menulis gambar terdekripsi ke file
def write_image(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)

# Fungsi untuk melakukan dekripsi pada gambar
def decrypt_image(encrypted_data, key, iv):
    # Melakukan dekripsi pada gambar
    decrypted_image_data = decrypt_AES_CBC(encrypted_data[AES.block_size:], key, iv)
    return decrypted_image_data

# Fungsi untuk mendekompresi gambar menggunakan Brotli
def decompress_image(input_path, output_path):
    with open(input_path, 'rb') as f_in:
        compressed_data = f_in.read()
        decompressed_data = brotli.decompress(compressed_data)

    with open(output_path, 'wb') as f_out:
        f_out.write(decompressed_data)

# Fungsi untuk memampatkan gambar menggunakan Brotli
def compress_image(input_path, output_path, quality=5):
    with open(input_path, 'rb') as f_in:
        image_data = f_in.read()
        compressed_data = brotli.compress(image_data, quality=quality)

    with open(output_path, 'wb') as f_out:
        f_out.write(compressed_data)

def embed_image(secret_image, cover_image, output_path):
    global original_secret_size

    # Convert both images to RGB mode if one of them is RGBA
    if cover_image.mode == 'RGBA':
        cover_image = cover_image.convert('RGB')
    if secret_image.mode == 'RGBA':
        secret_image = secret_image.convert('RGB')

    # Check if the secret image is grayscale
    if secret_image.mode == 'L':
        # Convert the cover image to grayscale if it's not already
        if cover_image.mode != 'L':
            cover_image = cover_image.convert('L')

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
                # Clear the last 3 LSBs of the cover pixel
                cover_pixels[y, x] &= ~7
                # Set the last 3 LSBs of the cover pixel to the corresponding bits of the secret image
                cover_pixels[y, x] |= (secret_pixels[y, x] >> 5) & 7

        # Save the resulting image
        embedded_image = Image.fromarray(cover_pixels)
        embedded_image.save(output_path)

        # Calculate PSNR and MSE
        mse = np.mean((secret_pixels - cover_pixels) ** 2)
        psnr = 20 * math.log10(255.0 / math.sqrt(mse))

        return psnr, mse

    else:  # If secret image is not grayscale
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
    # Check if the input image is grayscale
    if stego_image.mode == 'L':
        # If grayscale, convert it to RGB for processing
        stego_image = stego_image.convert('RGB')

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

    # Calculate PSNR and MSE
    secret_pixels = np.array(extracted_image)
    cover_pixels = np.array(stego_image)
    mse = np.mean((secret_pixels - cover_pixels) ** 2)
    psnr = 20 * math.log10(255.0 / math.sqrt(mse))

    return psnr, mse

class MyClass:
    def __init__(self, request):
        self.session = session
        self.request = request
        self.data = {
            'baseURL': request.base_url.rsplit('/', 1)[0],  # Mendapatkan base URL
        }

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', action='embed')

@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html', action='embed')

@app.route('/embed', methods=['GET'])
def stegano():
    return render_template('embed.html', action='embed')

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
            return render_template('embed.html', action='embed', output_image_name=os.path.basename(output_path), psnr=psnr, mse=mse)

        except Exception as e:
            return f'Error embedding image: {e}'

@app.route('/extract', methods=['GET'])
def destegano():
    return render_template('extract.html', action='extract')

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
            return render_template('extract.html', action='extract', extracted_image_name=os.path.basename(output_secret_path))

        except Exception as e:
            return f'Error extracting image: {e}'

@app.route('/encrypt', methods=['GET'])
def encryption():
    return render_template('encrypted.html', action='encrypt')

@app.route('/decrypt', methods=['GET'])
def decryption():
    return render_template('decrypted.html', action='decrypt')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        # Mendapatkan data dari request
        image_file = request.files['image']
        key = request.form['key']

        # Membaca data gambar
        image_data = image_file.read()

        # Melakukan enkripsi pada gambar
        encrypted_image = encrypt_image(image_data, key.encode())

        # Dapatkan timestamp saat ini sebagai bagian dari nama file
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_filename = f"static/encrypted_{timestamp}.png"

        # Menyimpan gambar terenkripsi
        # Mendapatkan format gambar dari nama file asli
        original_format = Image.open(io.BytesIO(image_data)).format
        # Menambahkan format gambar saat menyimpan
        with open(output_filename, 'wb') as f:
            f.write(encrypted_image)

        return jsonify({"message": "Encryption successful", "output_filename": output_filename})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        # Mendapatkan data dari request
        encrypted_image_file = request.files['image']
        key = request.form['key'].encode()

        # Membaca data gambar terenkripsi
        encrypted_image_data = encrypted_image_file.read()

        # Mengambil IV dari data terenkripsi
        iv = encrypted_image_data[:AES.block_size]

        # Melakukan dekripsi pada gambar
        decrypted_image_data = decrypt_image(encrypted_image_data, key, iv)

        # Dapatkan timestamp saat ini sebagai bagian dari nama file
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_filename = f"static/decrypted_{timestamp}.png"

        # Menyimpan gambar terdekripsi
        write_image(output_filename, decrypted_image_data)

        return jsonify({"message": "Decryption successful", "output_filename": output_filename})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/compress', methods=['GET'])
def compression():
    return render_template('compress.html', action='compress')

@app.route('/compress', methods=['POST'])
def compress():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_extension = os.path.splitext(file.filename)[1]
        input_path = f'static/uploaded_{timestamp}{file_extension}'
        file.save(input_path)
        
        output_path = f'static/compressed_{timestamp}{file_extension}.br'
        compress_image(input_path, output_path)

        # Hapus file input setelah dikompresi
        os.remove(input_path)

        output_image_name = os.path.basename(output_path)
        return jsonify({'output_image_name': output_image_name, 'success': True})
    
@app.route('/decompress', methods=['GET'])
def decompression():
    return render_template('decompress.html', action='compress')

if __name__ == '__main__':
    app.run(debug=True)