from Crypto.Cipher import AES
import os

def pad(data):
    padding_length = AES.block_size - len(data) % AES.block_size
    return data + bytes([padding_length] * padding_length)

def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_CBC, os.urandom(16))
    return cipher.encrypt(data)

def decrypt_data(encrypted_data, key):
    cipher = AES.new(key, AES.MODE_CBC, os.urandom(16))
    return cipher.decrypt(encrypted_data)
