#!usr/bin/env bash

set -e

if [ $# -ne 1 ]; then
    echo "Usage: ./1_create_uuid_table.sh <data-root>"
    echo "Writes an empty phone number <-> UUID table"
    exit
fi

DATA_DIR=$1

if [ -f "$DATA_DIR/UUIDs/phone_uuids.json" ]; then
    echo "Error: '$DATA_DIR/UUIDs/phone_uuids.json' already exists; refusing to overwrite."
    echo "    To generate a new, empty phone number <-> UUID table, delete phone_uuids.json file first."
    exit 1
fi

mkdir -p "$DATA_DIR/UUIDs"
echo "{}" > "$DATA_DIR/UUIDs/phone_uuids.json"
