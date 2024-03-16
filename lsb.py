from PIL import Image

def embed_message(secret_message, cover_image, output_path):
    secret_data = bytes(secret_message, 'utf-8')
    secret_size = len(secret_data)

    cover_pixels = cover_image.load()

    image_size = cover_image.size
    width, height = image_size

    if width * height < secret_size:
        raise ValueError("Cover image capacity is not enough to embed the secret message.")

    encoded_index = 0

    for y in range(height):
        for x in range(width):
            r, g, b = cover_pixels[x, y]

            if encoded_index < secret_size:
                cover_pixels[x, y] = r & ~1 | (secret_data[encoded_index] >> 7), \
                                     g & ~1 | ((secret_data[encoded_index] >> 6) & 1), \
                                     b & ~1 | ((secret_data[encoded_index] >> 5) & 1)
                encoded_index += 1

    cover_image.save(output_path)

def extract_message(stego_image_path):
    stego_image = Image.open(stego_image_path)
    stego_pixels = stego_image.load()

    width, height = stego_image.size

    extracted_message = []

    for y in range(height):
        for x in range(width):
            r, g, b = stego_pixels[x, y]
            extracted_message.append((r & 1) << 7 | (g & 1) << 6 | (b & 1) << 5)

    return bytes(extracted_message).decode('utf-8')
