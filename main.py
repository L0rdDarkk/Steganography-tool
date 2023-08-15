import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from PIL import Image

class ImageSteganographyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Steganography Tool')
        self.setGeometry(200, 200, 800, 600)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        main_layout = QVBoxLayout(self.centralWidget)
        main_layout.setAlignment(Qt.AlignCenter)

        self.addIcon(main_layout)

        self.imageLabel = QLabel(self)
        self.imageLabel.setFixedSize(400, 400)
        main_layout.addWidget(self.imageLabel)

        self.secretMessageTextEdit = QTextEdit(self)
        self.secretMessageTextEdit.setFixedSize(400, 100)
        main_layout.addWidget(self.secretMessageTextEdit)

        self.encodeButton = QPushButton('Encode', self)
        self.encodeButton.setFixedSize(150, 40)
        main_layout.addWidget(self.encodeButton)
        self.encodeButton.clicked.connect(self.encodeMessage)

        self.decodeButton = QPushButton('Decode', self)
        self.decodeButton.setFixedSize(150, 40)
        main_layout.addWidget(self.decodeButton)
        self.decodeButton.clicked.connect(self.decodeMessage)

        self.setFont(QFont('Helvetica', 12))

        self.show()

    def addIcon(self, layout):
        pixmap = QPixmap('/Users/apple/Documents/lord-projects/Steganography-tool/icon.png')
        icon_label = QLabel(self)
        icon_label.setPixmap(pixmap.scaled(400,300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(icon_label, alignment=Qt.AlignTop | Qt.AlignHCenter)

    def encodeMessage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        image_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)', options=options)

        if image_path:
            secret_message = self.secretMessageTextEdit.toPlainText()
            encrypted_message = self.encrypt(secret_message)
            encoded_image = self.encode_image(image_path, encrypted_message)
            self.display_image(encoded_image)

    def decodeMessage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        image_path, _ = QFileDialog.getOpenFileName(self, 'Open Encoded Image', '', 'Image Files (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)', options=options)

        if image_path:
            encoded_message = self.decode_image(image_path)
            decrypted_message = self.decrypt(encoded_message)
            self.secretMessageTextEdit.setPlainText(decrypted_message)

    def display_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.imageLabel.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))

    def encode_image(self, source_img_path, secret_msg):
        source_img = Image.open(source_img_path)
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
        encoded_img.save(output_img_path)
        print("Image encoded successfully.")
        return output_img_path

    def decode_image(self, encoded_img_path):
        encoded_img = Image.open(encoded_img_path)
        secret_msg_bin = ''

        for y in range(encoded_img.height):
            for x in range(encoded_img.width):
                pixel = encoded_img.getpixel((x, y))

                for color_channel in range(3):
                    secret_msg_bin += format(pixel[color_channel], '08b')[-1]

        return secret_msg_bin

    def encrypt(self, message):
        key = 3  # Caesar cipher key
        encrypted_message = ''.join(chr((ord(char) - key) % 256) for char in message)
        return encrypted_message

    def decrypt(self, encrypted_message):
        key = 3  # Caesar cipher key
        decrypted_message = ''.join(chr((ord(char) + key) % 256) for char in encrypted_message)
        return decrypted_message

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageSteganographyApp()
    sys.exit(app.exec_())
