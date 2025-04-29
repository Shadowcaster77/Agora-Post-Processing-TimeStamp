#!/bin/bash
# This script removes all files in the current directory and its subdirectories.
# It is used when the argument is too long for the rm command (too many files).

# protection in case of accidental execution
read -p "Delete EVERYTHING in this folder? (y/n) " confirm
if [[ "$confirm" == "y" ]]; then
  find . -type f | xargs rm
  echo "Deleted."
else
  echo "Cancelled."
  exit
fi

# the real deletion command (you can copy this if you know what you are doing)
# find . -type f | xargs rm
