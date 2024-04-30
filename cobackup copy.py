from flask import Flask, session, request, render_template, request, redirect, url_for, send_from_directory, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename
from datetime import datetime
import brotli
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import mean_squared_error as mse
import math
import pywt
import time
from io import BytesIO

app = Flask(__name__, static_folder='static')

# Fixed IV in 16-bit format
fixed_iv = "LugayaLuluss2024".encode('utf-8')[:16]

# Function to encrypt image
def encrypt_image(image, key, iv=fixed_iv, mode=AES.MODE_CBC):
    # Convert original image data to bytes
    imageOrigBytes = image.tobytes()

    # Encrypt
    cipher = AES.new(key, mode, iv)
    imageOrigBytesPadded = pad(imageOrigBytes, AES.block_size)
    ciphertext = cipher.encrypt(imageOrigBytesPadded)

    # Convert ciphertext bytes to encrypted image data
    paddedSize = len(imageOrigBytesPadded) - len(imageOrigBytes)
    void = image.shape[1] * image.shape[2] - len(iv) - paddedSize
    ivCiphertextVoid = iv + ciphertext + bytes(void)
    imageEncrypted = np.frombuffer(ivCiphertextVoid, dtype=image.dtype).reshape(image.shape[0] + 1, image.shape[1], image.shape[2])

    return imageEncrypted, mode, iv

# Function to decrypt image
def decrypt_image(image, key, iv=fixed_iv, mode=AES.MODE_CBC):
    # Convert encrypted image data to ciphertext bytes
    rowEncrypted, columnOrig, depthOrig = image.shape 
    rowOrig = rowEncrypted - 1
    encryptedBytes = image.tobytes()
    encrypted_iv = encryptedBytes[:len(iv)]
    encrypted_data = encryptedBytes[len(iv):]

    # Decrypt
    cipher = AES.new(key, mode, iv)
    decryptedImageBytesPadded = cipher.decrypt(encrypted_data)

    # Unpad decrypted data
    decryptedImageBytes = unpad(decryptedImageBytesPadded, AES.block_size)

    # Convert bytes to decrypted image data
    decryptedImage = np.frombuffer(decryptedImageBytes, image.dtype).reshape(rowOrig, columnOrig, depthOrig)

    return decryptedImage

# Fungsi untuk mendekompresi gambar menggunakan Brotli
def decompress_image(input_path, output_path):
    with open(input_path, 'rb') as f_in:
        compressed_data = f_in.read()
        decompressed_data = brotli.decompress(compressed_data)

    with open(output_path, 'wb') as f_out:
        f_out.write(decompressed_data)

def compress_image_with_dwt(input_path, output_path, compression_level=2):
    # Baca gambar menggunakan OpenCV
    img = cv2.imread(input_path)
    
    # Terapkan transformasi DWT (Discrete Wavelet Transform) pada setiap saluran warna
    coeffs = [pywt.dwt2(img[:,:,i], 'haar') for i in range(img.shape[2])]
    LLs, subbands = zip(*coeffs)
    
    # Quantisasi koefisien
    quantized_subbands = []
    for subband in subbands:
        quantized_subbands.append([np.round(coeff / (2**compression_level)) * (2**compression_level) for coeff in subband])
    
    # Rekonstruksi gambar dari koefisien yang telah dikuantisasi
    reconstructed_channels = [pywt.idwt2((LL, tuple(subband)), 'haar') for LL, subband in zip(LLs, quantized_subbands)]
    reconstructed_img = np.stack(reconstructed_channels, axis=-1)
    
    # Simpan gambar hasil kompresi
    cv2.imwrite(output_path, reconstructed_img)

def embed_image(secret_image, cover_image, output_path):
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

        # Save original secret size as metadata
        embedded_image.info['original_secret_size'] = original_secret_size

        embedded_image.save(output_path)

        # Calculate PSNR and MSE for embedded image compared to cover image
        mse_val = mse(cover_pixels.astype(float), np.array(cover_image).astype(float))
        psnr_val = psnr(cover_pixels.astype(float), np.array(cover_image).astype(float), data_range=255)

        return psnr_val, mse_val, original_secret_size

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

        # Save original secret size as metadata
        embedded_image.info['original_secret_size'] = original_secret_size

        embedded_image.save(output_path)

        # Calculate PSNR and MSE for embedded image compared to cover image
        mse_val = mse(cover_pixels.astype(float), np.array(cover_image).astype(float))
        psnr_val = psnr(cover_pixels.astype(float), np.array(cover_image).astype(float), data_range=255)

        return psnr_val, mse_val, original_secret_size
     
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
    stego_image.save(output_cover_path)

    # Calculate PSNR and MSE
    secret_pixels = np.array(extracted_image)
    cover_pixels = np.array(stego_image)
    mse = np.mean((secret_pixels - cover_pixels) ** 2)
    psnr = 20 * math.log10(255.0 / math.sqrt(mse))

    # Read original secret size from metadata
    original_secret_size = stego_image.info.get('original_secret_size')

    return psnr, mse, original_secret_size

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

            # Baca gambar rahasia
            secret_image = Image.open(secret_image_path)

            # Dapatkan timestamp saat ini sebagai bagian dari nama file
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

            # Path untuk menyimpan gambar stego yang disisipkan gambar rahasia
            output_path = f'static/embedded_{timestamp}.png'

            # Memanggil fungsi untuk menyembunyikan gambar rahasia
            psnr_val, mse_val, original_secret_size = embed_image(secret_image, Image.open(cover_image_path), output_path)

            # Mengirimkan nama file gambar yang dihasilkan, nilai PSNR, MSE, dan ukuran asli gambar rahasia ke template
            return render_template('embed.html', action='embed', output_image_name=os.path.basename(output_path), psnr=psnr_val, mse=mse_val, original_secret_size=original_secret_size)

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

            # Memanggil fungsi extract_image dengan original_secret_size
            psnr, mse, original_secret_size = extract_image(stego_image, output_cover_path, output_secret_path)

            # Redirect ke halaman utama setelah selesai
            return render_template('extract.html', action='extract', extracted_image_name=os.path.basename(output_secret_path), psnr=psnr, mse=mse, original_secret_size=original_secret_size)

        except Exception as e:
            return f'Error extracting image: {e}'
        
@app.route('/encrypt', methods=['GET'])
def encryption():
    return render_template('encrypted.html', action='encrypt')

@app.route('/decrypt', methods=['GET'])
def decryption():
    return render_template('decrypted.html', action='decrypt')

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)

        # Read uploaded image
        nparr = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Get key from user input
        key = request.form['key']

        # Encrypt image
        encrypted_image, mode, _ = encrypt_image(image, key.encode(), fixed_iv)

        # Save encrypted image temporarily
        _, buffer = cv2.imencode('.jpg', encrypted_image)
        encrypted_image_bytes = BytesIO(buffer)

        return send_file(encrypted_image_bytes, mimetype='image/jpeg', as_attachment=True, download_name='encrypted_image.jpg')

    return render_template('encrypt.html')

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)

        # Read uploaded image
        nparr = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Get key from user input
        key = request.form['key']

        # Decrypt image
        decrypted_image = decrypt_image(image, key.encode(), fixed_iv)

        # Save decrypted image temporarily
        _, buffer = cv2.imencode('.jpg', decrypted_image)
        decrypted_image_bytes = BytesIO(buffer)

        return send_file(decrypted_image_bytes, mimetype='image/jpeg', as_attachment=True, download_name='decrypted_image.jpg')

    return render_template('decrypt.html')
    
@app.route('/compress', methods=['GET'])
def compression():
    return render_template('compress.html', action='compress')

@app.route('/compress', methods=['POST'])
@app.route('/compress', methods=['POST'])
def compress_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        timestamp = int(time.time())
        file_extension = os.path.splitext(file.filename)[1]
        input_path = f'static/uploaded_{timestamp}{file_extension}'
        file.save(input_path)
        
        output_path = f'static/compressed_{timestamp}{file_extension}'
        
        # Mendapatkan nilai tingkat kompresi dari form HTML
        compression_level = int(request.form.get('compression_level', 5))
        
        compress_image_with_dwt(input_path, output_path, compression_level)

        # Hapus file input setelah dikompresi
        os.remove(input_path)

        output_image_name = os.path.basename(output_path)
        return jsonify({'output_image_name': output_image_name, 'success': True})
    
@app.route('/decompress', methods=['GET'])
def decompression():
    return render_template('decompress.html', action='compress')

if __name__ == '__main__':
    app.run(debug=True)