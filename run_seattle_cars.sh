#!/bin/bash

# Set up logging for the script
log_file="/home/ec2-user/seattle_cars_error.log"

# Run the Python script with the area set as a command-line argument (e.g., 5 for the fifth area set)
# Replace 5 with the area set number you want to use for each instance
python3 clBot/seattle_cars.py 5 >> "$log_file" 2>&1
