from flask import Flask, session, request, render_template, request, redirect, url_for, send_from_directory, jsonify, send_file
from flask_session import Session
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
import sys
import io
from io import BytesIO

app = Flask(__name__, static_folder='static')
# Configure session to use filesystem (you can also use other session backends)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

def decompress_image_with_dwt(input_path, output_path, compression_level=2):
    # Baca gambar yang telah dikompresi menggunakan OpenCV
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    
    # Gambar yang dibaca adalah gambar yang telah direkonstruksi dari koefisien yang dikuantisasi
    # Kita perlu memisahkan kembali saluran warna dan menerapkan invers DWT pada setiap saluran
    coeffs_from_img = [pywt.dwt2(img[:,:,i], 'haar') for i in range(img.shape[2])]
    LLs, subbands = zip(*coeffs_from_img)
    
    # Dekuantisasi subband tinggi frekuensi
    dequantized_subbands = []
    for subband in subbands:
        dequantized_subbands.append([band * (2**compression_level) for band in subband])
    
    # Rekonstruksi gambar dari koefisien yang telah didekuantisasi
    reconstructed_channels = [pywt.idwt2((LLs[i], tuple(dequantized_subbands[i])), 'haar') for i in range(len(LLs))]
    reconstructed_img = np.stack(reconstructed_channels, axis=-1)
    
    # Simpan gambar yang telah direkonstruksi
    cv2.imwrite(output_path, reconstructed_img)

def compress_image_with_dwt(input_path, output_path, compression_level=2):
    # Baca gambar menggunakan OpenCV
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    
    # Terapkan transformasi DWT (Discrete Wavelet Transform) pada setiap saluran warna
    coeffs = [pywt.dwt2(img[:,:,i], 'haar') for i in range(img.shape[2])]
    LLs, subbands = zip(*coeffs)
    
    # Kuantisasi hanya pada subband tinggi frekuensi
    quantized_subbands = []
    for subband in subbands:
        quantized_subbands.append([np.round(band / (2**compression_level)) * (2**compression_level) for band in subband])
    
    # Rekonstruksi gambar dari koefisien yang telah dikuantisasi
    reconstructed_channels = [pywt.idwt2((LLs[i], tuple(quantized_subbands[i])), 'haar') for i in range(len(LLs))]
    reconstructed_img = np.stack(reconstructed_channels, axis=-1)
    
    # Menentukan format berdasarkan ekstensi file asli
    file_extension = os.path.splitext(output_path)[1][1:].upper()  # Mengambil ekstensi dan mengubahnya menjadi format yang diterima oleh OpenCV
    if file_extension == 'JPG':
        file_extension = 'JPEG'  # OpenCV menggunakan JPEG bukan JPG
    cv2.imwrite(output_path, reconstructed_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100 - compression_level * 10] if file_extension == 'JPEG' else [])
    
def embed_image(secret_image, cover_image, output_path, use_aes=False, password=None):
    if use_aes and not password:
        raise ValueError("Password is required for AES encryption.")

    # Convert both images to RGB mode if one of them is RGBA
    if cover_image.mode == 'RGBA':
        cover_image = cover_image.convert('RGB')
    if secret_image.mode == 'RGBA':
        secret_image = secret_image.convert('RGB')

    # Resize the secret image to match the cover image size by padding with black color
    cover_width, cover_height = cover_image.size
    secret_width, secret_height = secret_image.size

    if secret_width != cover_width or secret_height != cover_height:
        new_secret_image = Image.new('RGB', (cover_width, cover_height), (0, 0, 0))
        new_secret_image.paste(secret_image, ((cover_width - secret_width) // 2, (cover_height - secret_height) // 2))
        secret_image = new_secret_image

    # Convert images to numpy arrays
    secret_pixels = np.array(secret_image)
    cover_pixels = np.array(cover_image)

    if use_aes:
        # Encrypt the secret image using AES in CBC mode
        cipher = AES.new(password.encode(), AES.MODE_CBC, b'0000000000000000')
        secret_bytes = pad(secret_pixels.tobytes(), AES.block_size)
        encrypted_secret_bytes = cipher.encrypt(secret_bytes)
        # Reshape the encrypted bytes to match the dimensions of the secret image
        secret_pixels = np.frombuffer(encrypted_secret_bytes, dtype=np.uint8)
        secret_pixels = secret_pixels[:cover_width * cover_height * 3]  # Ensure it fits into the cover image
        secret_pixels = secret_pixels.reshape((cover_height, cover_width, 3))

# Embed the secret image into the cover image using LSB with increased bits
    for y in range(cover_height):
        for x in range(cover_width):
            for c in range(3):  # RGB channels
                # Clear the last 3 LSBs of the cover pixel
                cover_pixels[y, x, c] = cover_pixels[y, x, c] & (~7)
                # Set the last 3 LSBs of the cover pixel to the corresponding bits of the secret image
                cover_pixels[y, x, c] = (cover_pixels[y, x, c] | ((secret_pixels[y, x, c] >> 5) & 7)).astype(np.uint8)

    # Save the resulting image
    embedded_image = Image.fromarray(cover_pixels)

    # Save original secret size as metadata
    embedded_image.info['original_secret_size'] = (secret_width, secret_height)

    # Save password as metadata if AES is used
    if use_aes:
        embedded_image.info['password'] = password

    embedded_image.save(output_path)

    # Calculate PSNR and MSE for embedded image compared to cover image
    mse_val = mse(cover_pixels.astype(float), np.array(cover_image).astype(float))
    psnr_val = psnr(cover_pixels.astype(float), np.array(cover_image).astype(float), data_range=255)

    return psnr_val, mse_val, (secret_width, secret_height)

def extract_image(stego_image, output_cover_path, output_secret_path, use_aes=False, password=None):
    if use_aes and not password:
        raise ValueError("Password is required for AES decryption.")

    # Convert stego image to RGB mode if it's RGBA
    if stego_image.mode == 'RGBA':
        stego_image = stego_image.convert('RGB')

    # Get dimensions of the stego image
    width, height = stego_image.size

    # Create a numpy array to store the extracted secret image
    extracted_pixels = np.zeros((height, width, 3), dtype=np.uint8)

    # Extract the secret image from the stego image using LSB with increased bits for each color channel
    stego_pixels = np.array(stego_image)
    for y in range(height):
        for x in range(width):
            for c in range(3):  # RGB channels
                # Extract the last 3 bits from the stego image pixel and shift them to the correct position
                extracted_pixels[y, x, c] = (stego_pixels[y, x, c] & 7) << 5

    # If AES decryption is enabled, perform decryption
    if use_aes:
        try:
            # Decrypt the secret image using AES in CBC mode
            cipher = AES.new(password.encode(), AES.MODE_CBC, b'0000000000000000')
            secret_bytes = extracted_pixels.tobytes()
            decrypted_secret_bytes = cipher.decrypt(secret_bytes)
            # Unpad the decrypted bytes
            decrypted_secret_bytes = unpad(decrypted_secret_bytes, AES.block_size)
            # Reshape the decrypted bytes to match the dimensions of the secret image
            secret_pixels = np.frombuffer(decrypted_secret_bytes, dtype=np.uint8)
            # Reshape considering the image may have been padded to be square
            secret_pixels = secret_pixels[:height * width * 3]  # Ensure it fits into the extracted image
            secret_pixels = secret_pixels.reshape((height, width, 3))
            decrypted_secret_image = Image.fromarray(secret_pixels)
            decrypted_secret_image.save(output_secret_path)
        except ValueError as e:
            print(f"Error during decryption: {e}")
            return
    else:
        # Save the extracted secret image directly
        extracted_image = Image.fromarray(extracted_pixels)
        extracted_image.save(output_secret_path)

    # Save the extracted cover image as is
    stego_image.save(output_cover_path)

    # # Calculate PSNR and MSE
    # secret_pixels = np.array(extracted_image)
    # cover_pixels = np.array(stego_image)
    # mse = np.mean((secret_pixels - cover_pixels) ** 2)
    # psnr = 20 * math.log10(255.0 / math.sqrt(mse))

    # return psnr, mse

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
            # secret_image_extension = os.path.splitext(secret_image.filename)[1]
            # output_path = f'static/embedded_{timestamp}{secret_image_extension}'
            output_path = f'static/embedded_{timestamp}.png'

            # Periksa apakah opsi AES Encryption dicentang
            use_aes = False
            if 'use_aes' in request.form:
                use_aes = True
                password = request.form['password']
            else:
                password = None

            # Memanggil fungsi untuk menyembunyikan gambar rahasia
            psnr_val, mse_val, original_secret_size = embed_image(secret_image, Image.open(cover_image_path), output_path, use_aes=use_aes, password=password)

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
            # stego_image_extension  = os.path.splitext(stego_image.filename)[1]
            # output_secret_path = f'static/extracted_secret_{timestamp}{stego_image_extension}'
            # output_cover_path = f'static/extracted_cover_{timestamp}{stego_image_extension}'
            output_secret_path = f'static/extracted_secret_{timestamp}.png'
            output_cover_path = f'static/extracted_cover_{timestamp}.png'

            # # Ambil input untuk lebar dan tinggi asli gambar rahasia
            # original_width = int(request.form['original_width'])  # Konversi menjadi integer
            # original_height = int(request.form['original_height'])  # Konversi menjadi integer

            # Periksa apakah opsi AES Encryption dicentang
            use_aes = False
            if 'use_aes' in request.form:
                use_aes = True
                password = request.form['password']
            else:
                password = None

            # Memanggil fungsi extract_image dengan original_secret_size
            extract_image(stego_image, output_cover_path, output_secret_path, use_aes=use_aes, password=password)

            # Redirect ke halaman utama setelah selesai
            return render_template('extract.html', action='extract', extracted_image_name=os.path.basename(output_secret_path))

        except Exception as e:
            return f'Error extracting image: {e}'
        
# @app.route('/encrypt', methods=['GET'])
# def encryption():
#     return render_template('encrypted.html', action='encrypt')

# @app.route('/decrypt', methods=['GET'])
# def decryption():
#     return render_template('decrypted.html', action='decrypt')

# # Set mode
# mode = AES.MODE_CBC
# # mode = AES.MODE_ECB
# if mode != AES.MODE_CBC and mode != AES.MODE_ECB:
#     print('Only CBC and ECB mode supported...')
#     sys.exit()

# # Set sizes
# keySize = 32
# ivSize = AES.block_size if mode == AES.MODE_CBC else 0

# @app.route('/upload', methods=['POST'])
# def upload():
#     uploaded_file = request.files['file']
#     if uploaded_file.filename != '':
#         # Save the uploaded file to a temporary location
#         file_path = os.path.join('uploads', uploaded_file.filename)
#         uploaded_file.save(file_path)

#         # Read the uploaded image
#         imageOrig = cv2.imread(file_path)
#         rowOrig, columnOrig, depthOrig = imageOrig.shape

#         # Check for minimum width
#         minWidth = (AES.block_size + AES.block_size) // depthOrig + 1
#         if columnOrig < minWidth:
#             return 'The minimum width of the image must be {} pixels, so that IV and padding can be stored in a single additional row!'.format(minWidth)

#         # Convert original image data to bytes
#         imageOrigBytes = imageOrig.tobytes()

#         # Encrypt
#         key = get_random_bytes(keySize)
#         iv = get_random_bytes(ivSize)
#         cipher = AES.new(key, AES.MODE_CBC, iv) if mode == AES.MODE_CBC else AES.new(key, AES.MODE_ECB)
#         imageOrigBytesPadded = pad(imageOrigBytes, AES.block_size)
#         ciphertext = cipher.encrypt(imageOrigBytesPadded)

#         # Convert ciphertext bytes to encrypted image data
#         paddedSize = len(imageOrigBytesPadded) - len(imageOrigBytes)
#         void = columnOrig * depthOrig - ivSize - paddedSize
#         ivCiphertextVoid = iv + ciphertext + bytes(void)
#         imageEncrypted = np.frombuffer(ivCiphertextVoid, dtype=imageOrig.dtype).reshape(rowOrig + 1, columnOrig, depthOrig)

#         # Delete the temporary file
#         os.remove(file_path)

#         # Pass encrypted image data to the template
#         return render_template('encrypted.html', encrypted_image=imageEncrypted)
#     else:
#         return 'No file uploaded!'

# @app.route('/display_encrypted_image')
# def display_encrypted_image():
#     # Retrieve encrypted image from the session
#     encrypted_image = session.get('encrypted_image')
#     print("Encrypted image:", encrypted_image)  # Add this line for debugging
#     if encrypted_image is not None:
#         # Convert encrypted image data to bytes
#         encrypted_image_bytes = encrypted_image.tobytes()
#         # Send the encrypted image data as a file
#         return send_file(io.BytesIO(encrypted_image_bytes), mimetype='image/jpeg')
#     else:
#         return 'Encrypted image not found!'

# @app.route('/decrypt', methods=['GET', 'POST'])
# def decrypt():
#     if request.method == 'POST':
#         if 'image' not in request.files:
#             return redirect(request.url)
#         file = request.files['image']
#         if file.filename == '':
#             return redirect(request.url)

#         # Read uploaded image
#         nparr = np.frombuffer(file.read(), np.uint8)
#         image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#         # Get key from user input
#         key = request.form['key']

#         # Decrypt image
#         decrypted_image = decrypt_image(image, key.encode(), fixed_iv)

#         # Save decrypted image temporarily
#         _, buffer = cv2.imencode('.jpg', decrypted_image)
#         decrypted_image_bytes = BytesIO(buffer)

#         return send_file(decrypted_image_bytes, mimetype='image/jpeg', as_attachment=True, download_name='decrypted_image.jpg')

#     return render_template('decrypt.html')
    
@app.route('/compress', methods=['GET'])
def compression():
    return render_template('compress.html', action='compress')

@app.route('/compress', methods=['POST'])
def compress_image():
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
        
        output_path = f'static/compressed_{timestamp}{file_extension}'  # Menggunakan ekstensi asli
        
        compression_level = int(request.form.get('compression_level', 5))
        
        # Memanggil fungsi kompresi DWT yang telah diperbarui
        compress_image_with_dwt(input_path, output_path, compression_level)

        # Memeriksa apakah gambar berhasil disimpan sebelum menghapus gambar asli
        if os.path.exists(output_path):
            # Hapus file input setelah dikompresi
            os.remove(input_path)
            output_image_name = os.path.basename(output_path)
            return jsonify({'output_image_name': output_image_name, 'success': True})
        else:
            return jsonify({'error': 'Failed to compress image'})
    
@app.route('/decompress', methods=['GET'])
def decompression():
    return render_template('decompress.html', action='compress')

if __name__ == '__main__':
    app.run(debug=True)