#!/bin/bash

# This script is used to watch for changes in the tests.py file and run the tests
# when the file is modified.

# Store the absolute path of the script directory in a variable
script_dir=$(realpath "$(dirname "$0")")

echo "Watching $script_dir/tests.py for changes..."

inotifywait -q -m -e close_write "$script_dir/tests.py" |
while read -r; do
   python "$script_dir/tests.py"
done