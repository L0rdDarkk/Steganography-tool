# Find Me

A Python-based steganography tool for hiding and extracting information within images.

## Introduction

This Steganography Tool is designed to encode and decode hidden messages within image files. It provides a simple yet effective way to conceal sensitive information using various steganographic techniques.

## Features

- **Encode:** Hide text or binary data within an image.
- **Decode:** Extract hidden information from encoded images.
- **Multiple Techniques:** Support for various steganographic methods.
- **User-friendly Interface:** Easy-to-use command-line interface.

## Getting Started

### Prerequisites

Make sure you have Python (3.x recommended) installed.

### Installation

1. Clone the repository:
   git clone https://github.com/L0rdDarkk/Steganography-tool.git
Navigate to the project directory:
cd Steganography-tool

Install dependencies:
pip install -r requirements.txt

Usage
Encode a Message
python steganography.py encode --input <input_image_path> --output <output_image_path> --message "your secret message"
Decode a Message
python steganography.py decode --input <encoded_image_path>
For more options and help, run:


python steganography.py --help

Examples

Encoding:
python steganography.py encode --input original_image.png --output encoded_image.png --message "Hello, this is a secret message!"
Decoding:
python steganography.py decode --input encoded_image.png
