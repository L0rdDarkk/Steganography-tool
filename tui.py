import sys
from PIL import Image

class TextSteganographyApp:
    def __init__(self):
        self.initUI()

    def initUI(self):
        print("Welcome to Steganography Tool")
        print("-------------------------------")
        self.encodeMessage()

    def encodeMessage(self):
        image_path = input("Enter the path of the image to encode: ")
        secret_message = input("Enter the secret message: ")
        encrypted_message = self.encrypt(secret_message)
        encoded_image_path = self.encode_image(image_path, encrypted_message)
        print(f"Encoded image saved at {encoded_image_path}")

    def encode_image(self, source_img_path, secret_msg):
    

        output_img_path = "encoded_image.png"
        
        return output_img_path

    def encrypt(self, message):
        key = 3  # Caesar cipher key
        encrypted_message = ''.join(chr((ord(char) - key) % 256) for char in message)
        return encrypted_message

if __name__ == '__main__':
    app = TextSteganographyApp()
