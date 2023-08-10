'''
This script reads the config json file, update fields based on argument, and
write the results to default file path.

* Note: This script overwrites the default json file!
'''

import json
import re
from optparse import OptionParser
from tabulate import tabulate

# Input/output files
PROJ_PATH = '/home/ct297/workspace/agora_single-core-sim/'
FILE_PATH= 'files/config/ci/'
R_FILE_NAME = 'tddconfig-sim-ul-fr2.json'
W_FILE_NAME = 'tddconfig-sim-ul-fr2-autogen.json'

################################################################################
# JSON operations
################################################################################

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

def modify_json_data(data, mu, code_rate, modulation, num_worker, num_uplink):
    '''
    Acceptable parameter ranges:
        mu: 0-3, int
        code_rate: 0-1, often 0.333, 0.5 or 0.666
        modulation: 16QAM or 64QAM
    '''
    # Modify the JSON data as needed
    # data['updated'] = True
    data['sample_rate'] = get_sample_rate(mu=mu, fft_size=data['fft_size'])
    data['ul_mcs']['modulation'] = modulation
    data['ul_mcs']['code_rate'] = code_rate
    data['dl_mcs']['modulation'] = modulation
    data['dl_mcs']['code_rate'] = code_rate
    data['worker_thread_num'] = check_single_core_setup(num_worker)
    data['frame_schedule'] = [gen_frame_shedule(num_uplink=num_uplink)]

def write_json_file(data, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

################################################################################
# Print functions
################################################################################

def print_dict_as_table(dictionary):
    # Convert the dictionary to a list of key-value pairs
    table_data = [[key, value] for key, value in dictionary.items()]

    # Print the table
    print(tabulate(table_data, headers=["Key", "Value"], tablefmt="grid"))

################################################################################
# 5G related setting
################################################################################

def get_sample_rate(mu, fft_size):
    '''
    mu0 = 15 kHz, mu1 = 30 kHz, mu2 = 60 kHz, mu3 = 120 kHz
    sample_rate = mu * fft_size
    mu0: 15.36e6, mu1: 30.72e6, mu2: 61.44e6, mu3: 122.88e6 if fft_size = 1024
    '''
    return 15e3 * fft_size * 2 ** mu

def gen_frame_shedule(num_uplink):
    '''
    example: frame_schedule = 'PUUUGGGGGGGGGG'
    len(frame_schedule) = 14 and must start with P (pilot)
    '''
    if num_uplink not in range(0, 14):
        print('Error: num_uplink must be in range (0, 14), but get {}'.format(num_uplink))
        exit(0)
    frame_shedule = 'P' + num_uplink * 'U' + (13-num_uplink) * 'G'
    return frame_shedule

def check_single_core_setup(num_worker):
    if num_worker == 0:
        print('Warning: setting number of worker thread to 1 for single-core implimentation')
        print('Please check the Agora version or path is correct.')
        return 1
    return num_worker

################################################################################
# Main function
################################################################################

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-u", "--mu", type="int", dest="mu", help="Numerology [0-3], default=0", default=0)
    parser.add_option("-r", "--code_rate", type="float", dest="cr", help="Code rate [0-1], default=0.333", default=0.333)
    parser.add_option("-w", "--num_worker", type="int", dest="num_worker", help="Numer of worker threads, default=0", default=0)
    parser.add_option("-c", "--config_idx", type="int", dest="config_idx", help="Config index [0-3], default=0", default=0)
    parser.add_option("-m", "--modulation", type="string", dest="mod", help="Modulation scheme, default=16QAM", default='16QAM')
    parser.add_option("--num_uplink", type="int", dest="num_uplink", help="Number of uplink symbols [0-13], default=3", default=3)
    parser.add_option("--agora_dir", type="string", dest="proj_path", help="Path to compiled Agora, default={}".format(PROJ_PATH), default=PROJ_PATH)
    (options, args) = parser.parse_args()
    mu = options.mu
    cr = options.cr
    mod = options.mod
    num_worker = options.num_worker
    config_idx = options.config_idx
    num_uplink = options.num_uplink
    proj_path = options.proj_path

    read_json_file_path = proj_path + FILE_PATH + R_FILE_NAME
    write_json_file_path = proj_path + FILE_PATH + W_FILE_NAME

    # Read the JSON data from the file
    json_str = read_json_file_as_str(read_json_file_path)

    # Remove comments from the JSON data
    json_str = remove_json_comments(json_str)

    # Load the JSON data without comments into a dictionary
    json_data = json.loads(json_str)

    print('Read config: {}'.format(read_json_file_path))
    # print_dict_as_table(json_data)
    modify_json_data(data=json_data, mu=mu, code_rate=cr, modulation=mod, num_worker=num_worker, num_uplink=num_uplink)
    print('Generate json to {}'.format(write_json_file_path))
    print_dict_as_table(json_data)

    # Write the updated JSON data back to the file
    write_json_file(json_data, write_json_file_path)

    # print("JSON config {} has been modified and saved.".format(json_file_path))
