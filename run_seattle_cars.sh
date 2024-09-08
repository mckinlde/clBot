#!/bin/bash

# Set up logging for the script
log_file="/home/ec2-user/seattle_cars_error.log"

# Check if an area set number is provided
if [ -z "$1" ]; then
  echo "Error: No area set number provided." >> "$log_file"
  exit 1
fi

# Run the Python script with the area set number passed as a command-line argument
python3 clBot/seattle_cars.py "$1" >> "$log_file" 2>&1
