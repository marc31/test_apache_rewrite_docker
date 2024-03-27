#!/bin/bash

# This script is used to watch for changes in the conf/my_vhost.conf file 
# and reload the Apache web server when the file is modified.

# Store the absolute path of the script directory in a variable
script_dir=$(realpath "$(dirname "$0")")

echo "Watching $script_dir/conf/my_vhost.conf for changes..."

inotifywait -q -m -e close_write "$script_dir/conf/my_vhost.conf" |
while read -r filename event; do
   docker compose exec -T apache /bin/bash -c "/opt/bitnami/scripts/apache/reload.sh"
   echo "File $filename changed with event $event"
done