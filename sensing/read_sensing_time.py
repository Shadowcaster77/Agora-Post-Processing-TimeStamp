################################################################################
# Read from the savannah log to either
#   1) summarize the max and avg for each TF plot (ping-pong buffer size), and
#      give the overall average and max.
#   2) store the time into csv.
#
# Note that the file reads the latest log file from a folder path to simplify
# the experiment.
#
# Author: Chung-Hsuan Tung
################################################################################

import os
import re
from collections import defaultdict
import csv

# ==== Configuration ====
folder_path = "../../savannah_isac/log/"

# ==== Find latest modified file ====
def find_latest_file(folder):
    files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if not files:
        raise FileNotFoundError("No files found in the specified folder.")
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

# ==== Extract and group log data ====
def parse_log(file_path):
    frame_times = defaultdict(list)
    pattern = re.compile(r'DoSensingFreq\[\d+\]: \(Frame (\d+),.*?done with time ([\d.]+) ms')

    with open(file_path, 'r') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                frame_id = int(match.group(1))
                time_val = float(match.group(2))
                frame_times[frame_id].append(time_val)

    return frame_times

# ==== Main ====
def list_avg_max():
    try:
        latest_file = find_latest_file(folder_path)
        print(f"Reading from latest file: {latest_file}\n")

        frame_times = parse_log(latest_file)
        avg_list = []
        max_list = []

        for frame_id, times in frame_times.items():
            avg_time = sum(times) / len(times)
            max_time = max(times)
            avg_list.append(avg_time)
            max_list.append(max_time)

            print(f"Frame {frame_id}:")
            for t in times:
                print(f"  - {t:.4f} ms")
            print(f"  → Average: {avg_time:.4f} ms")
            print(f"  → Maximum: {max_time:.4f} ms\n")

        # Summary across all frame groups
        if avg_list:
            overall_avg = sum(avg_list) / len(avg_list)
            overall_max = max(max_list)
            print("=== Summary Across Frames ===")
            print(f"Total frames: {len(frame_times)}")
            print(f"Average of per-frame averages: {overall_avg:.4f} ms")
            print(f"Maximum of per-frame maximums: {overall_max:.4f} ms")

    except Exception as e:
        print(f"Error: {e}")

def store_time_to_csv():
    config_name = input('the config name: ')
    try:
        latest_file = find_latest_file(folder_path)
        print(f"Reading from latest file: {latest_file}\n")

        frame_times = parse_log(latest_file)
        print(frame_times)

        # collect all times together
        aggregated_times = []
        for key in frame_times:
            aggregated_times.extend(frame_times[key])
        print(aggregated_times)

        with open(config_name, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(aggregated_times)

        print(f"Data written to {config_name} successfully with length {len(aggregated_times)}.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # list_avg_max()
    store_time_to_csv()
