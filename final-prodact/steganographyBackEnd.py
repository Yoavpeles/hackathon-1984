from PIL import Image

def inspect_image(image_path):
    img = Image.open(image_path)
    print(f"Image Size: {img.size}")
    print(f"Pixel Data: {list(img.getdata())[:10]}")


def text_to_binary(message):
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    return binary_message + '1111111111111110'  # End delimiter

def embed_message(image_path, message, output_path):
    img = Image.open(image_path)
    binary_message = text_to_binary(message)

    if len(binary_message) > img.width * img.height * 3:
        raise ValueError("Message is too large to fit in the image.")

    encoded = img.copy()
    pixels = encoded.load()
    data_index = 0

    for y in range(img.height):
        for x in range(img.width):
            pixel = list(pixels[x, y])
            for i in range(3):  # Modify R, G, B channels
                if data_index < len(binary_message):
                    pixel[i] = pixel[i] & ~1 | int(binary_message[data_index])
                    data_index += 1
            pixels[x, y] = tuple(pixel)
            if data_index >= len(binary_message):
                break
        if data_index >= len(binary_message):
            break

    encoded.save(output_path)

def extract_binary(image_path):
    img = Image.open(image_path)
    pixels = img.load()
    binary_data = ""

    for y in range(img.height):
        for x in range(img.width):
            pixel = pixels[x, y]
            for i in range(3):  # Extract from R, G, B channels
                binary_data += str(pixel[i] & 1)

    return binary_data

def binary_to_text(binary_data):
    bytes_data = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message = ""
    for byte in bytes_data:
        if byte == "11111110":  # End delimiter
            break
        message += chr(int(byte, 2))
    return message[:-1]

def decode_message(image_path):
    binary_data = extract_binary(image_path)
    return binary_to_text(binary_data)


def main():
    while True:
        print("\nWelcome to the Encoder/Decoder!")
        mode = input("Enter mode (encode/decode or 'quit' to exit): ").strip().lower()
        
        if mode == "encode":
            image_path = input("Enter image file path: ")
            message = input("Enter message to hide: ")
            output_path = input("Enter output image file path: ")
            embed_message(image_path, message, output_path)
            print("Message encoded and saved.")
        elif mode == "decode":
            image_path = input("Enter encoded image file path: ")
            print("Hidden message:", decode_message(image_path))
        elif mode in ("quit", "exit"):
            print("Goodbye!")
            break
        else:
            print("Invalid mode selected. Please try again.")
if __name__ == "__main__":
    main()