################################################################################
# Helper functions to deal with reading data/metadata from files.
#
# Author: Chung-Hsuan Tung
################################################################################

import struct
import json
import yaml
import re

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

def read_yaml_file(file_path):
    """
    Reads a YAML file and returns the data as a Python dictionary."

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        dict: The YAML data as a Python dictionary, or None if an error occurs.
    """
    with open(file_path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            return data
        except yaml.YAMLError as e:
            print(f"Error reading YAML file: {e}")
            return None

# The following two function are used to tackle the file with comments
# The comments are removed before parsing the JSON file
def read_json_file_as_str(file_path):
    with open(file_path, 'r') as json_file:
        data = json_file.read()
    return data

def remove_json_comments(json_str):
    # Use a regular expression to remove single-line comments
    json_str = re.sub(r"(?m)^\s*//.*$", "", json_str)
    
    # Use a regular expression to remove multi-line comments
    json_str = re.sub(r"/\*.*?\*/", "", json_str, flags=re.DOTALL)

    return json_str

def read_json_file_no_comments(json_file_path):
    # Read the JSON data from the file
    json_str = read_json_file_as_str(json_file_path)

    # Remove comments from the JSON data
    json_str = remove_json_comments(json_str)

    # Load the JSON data without comments into a dictionary
    json_data = json.loads(json_str)

    return json_data
