#!/bin/bash
# Scipt Name: rfsynth_concatenate_raw_iq.sh
# Description: Concatenate the raw IQ files for each conofig from rfsynth for
#              large scale evaluation.
# Author: Chung-Hsuan Tung

FILE_PATH="../../savannah_isac/files/experiment/"

# Define a list (array) of files
FILES=("sparse.32cf" "test.32cf" "std.32cf" "dense.32cf" "dense_ds3.32cf")

# Output file
OUTPUT="combined_100mhz.32cf"

# Clear output file if it exists
> "$OUTPUT"

# Concatenate each file in the list
for FILE in "${FILES[@]}"; do
    cat "$FILE_PATH$FILE" >> "$FILE_PATH$OUTPUT"
done

echo "Files concatenated into $OUTPUT"
