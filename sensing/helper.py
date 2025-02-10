################################################################################
# Helper functions to deal with reading data/metadata from files.
#
# Author: Chung-Hsuan Tung
################################################################################

import struct
import json

def read_complex_samples(file_path):
    """
    Reads a binary file containing complex samples and returns them as a list of
    complex numbers.

    Args:
        file_path (str): The path to the binary file.

    Returns:
        list: A list of complex numbers, or None if an error occurs.
    """
    complex_values = []
    try:
        with open(file_path, 'rb') as file:
            while True:
                # Read two 32-bit floats (real and imaginary parts)
                data = file.read(8)  # 4 bytes for real, 4 bytes for imaginary
                if not data:
                    break
                # Unpack the binary data
                real, imag = struct.unpack('ff', data)  # 'ff' means two floats
                complex_values.append(complex(real, imag))
        return complex_values
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None

def read_json_file(file_path):
    """
    Reads a JSON file and returns the data as a Python dictionary.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The JSON data as a Python dictionary, or None if an error occurs.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return None
