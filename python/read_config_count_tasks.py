'''
This file reads the json config and compute the number of tasks in each stage.
'''

import json
import re
from tabulate import tabulate

# Input/output files
# PROJ_PATH = '/home/ct297/workspace/agora_origin/'
PROJ_PATH = '/home/ct297/workspace/agora_single-core-sim/'
FILE_PATH= PROJ_PATH + 'files/config/ci/'
FILE_NAME = 'tddconfig-sim-ul-fr2.json'

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

def count_tasks(config):
    num_task_per_stage = {}
    frame_schedule = config['frame_schedule'][0] # Extract str from list
    num_uplink_sym = frame_schedule.count('U')
    num_ofdm_data_subcarrier = config['ofdm_data_num']
    beam_block_size = config['beam_blcok_size'] if 'beam_block_size' in config else 8
    
    num_task_per_stage['FFT'] = num_uplink_sym
    num_task_per_stage['CSI'] = config['bs_radio_num'] * config['ue_radio_num']
    num_task_per_stage['BW'] = num_ofdm_data_subcarrier / beam_block_size
    num_task_per_stage['Demul'] = num_uplink_sym * num_ofdm_data_subcarrier
    num_task_per_stage['Decode'] = num_uplink_sym

    return num_task_per_stage

def print_dict_as_table(dictionary, headers):
    # Convert the dictionary to a list of key-value pairs
    table_data = [[key, value] for key, value in dictionary.items()]

    # Print the table
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    json_file_path = FILE_PATH + FILE_NAME

    # Read the JSON data from the file
    json_str = read_json_file_as_str(json_file_path)

    # Remove comments from the JSON data
    json_str = remove_json_comments(json_str)

    # Load the JSON data without comments into a dictionary
    json_data = json.loads(json_str)

    num_task_per_stage = count_tasks(json_data)

    print('Reading path: {}'.format(FILE_PATH))
    print('Reading log: {}'.format(FILE_NAME))
    # print_dict_as_table(json_data, ["Key", "Value"])
    print_dict_as_table(num_task_per_stage, ["Stage", "# of Tasks"])
