import sys
from PIL import Image

class TextSteganographyApp:
    def __init__(self):
        self.initUI()

    def initUI(self):
        print("Steganography-Tool")
        print("-------------------------------")
        choice = input("1. Encode\n2. Decode\nChoose an option (1/2): ")
        
        if choice == '1':
            self.encodeMessage()
        elif choice == '2':
            self.decodeMessage()
        else:
            print("Invalid choice. Please select 1 or 2.")

    def encodeMessage(self):
        image_path = input("Enter the path of the PNG image to encode: ")
        secret_message = input("Enter the secret message: ")
        encrypted_message = self.encrypt(secret_message)
        encoded_image_path = self.encode_image(image_path, encrypted_message)
        print(f"Encoded image saved at {encoded_image_path}")

    def decodeMessage(self):
        encoded_image_path = input("Enter the path of the encoded PNG image: ")
        decoded_message = self.decode_image(encoded_image_path)
        decrypted_message = self.decrypt(decoded_message)
        print(f"Decoded message: {decrypted_message}")

    def encode_image(self, source_img_path, secret_msg):
        source_img = Image.open(source_img_path).convert("RGBA")
        secret_msg = secret_msg + "\n"

        if len(secret_msg) > source_img.width * source_img.height:
            raise ValueError("Secret message is too long to encode in the image.")

        encoded_img = source_img.copy()

        secret_msg_bin = ''.join(format(ord(char), '08b') for char in secret_msg)
        secret_msg_idx = 0

        for y in range(source_img.height):
            for x in range(source_img.width):
                pixel = list(encoded_img.getpixel((x, y)))

                for color_channel in range(3):
                    if secret_msg_idx < len(secret_msg_bin):
                        pixel[color_channel] = int(format(pixel[color_channel], '08b')[:-1] + secret_msg_bin[secret_msg_idx], 2)
                        secret_msg_idx += 1

                encoded_img.putpixel((x, y), tuple(pixel))

                if secret_msg_idx >= len(secret_msg_bin):
                    break

        output_img_path = "encoded_image.png"
        encoded_img.save(output_img_path, "PNG")
        return output_img_path

    def decode_image(self, encoded_img_path):
        encoded_img = Image.open(encoded_img_path).convert("RGBA")
        secret_msg_bin = ''
        secret_byte = ''

        for y in range(encoded_img.height):
            for x in range(encoded_img.width):
                pixel = encoded_img.getpixel((x, y))

                for color_channel in range(3):
                    secret_byte += format(pixel[color_channel], '08b')[-1]

                    if len(secret_byte) == 8:
                        if secret_byte == '00000000':  # End of message indicator
                            break
                        secret_msg_bin += secret_byte
                        secret_byte = ''

                if secret_byte == '00000000':
                    break

        secret_message = ''
        for i in range(0, len(secret_msg_bin), 8):
            secret_message += chr(int(secret_msg_bin[i:i+8], 2))

        return secret_message

    def encrypt(self, message):
        key = 3
        encrypted_message = ''.join(chr((ord(char) - key) % 256) for char in message)
        return encrypted_message

    def decrypt(self, encrypted_message):
        key = 3  
        decrypted_message = ''.join(chr((ord(char) + key) % 256) for char in encrypted_message)
        return decrypted_message

if __name__ == '__main__':
    app = TextSteganographyApp()
