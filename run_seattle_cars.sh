#!/bin/bash

# Set the log file for capturing stdout and stderr
LOG_FILE="/home/ec2-user/seattle_cars_error.log"

# Determine which area set to use by passing it as an argument
# You can pass the area set (1, 2, 3, 4, 5) to the script.
if [ -z "$1" ]; then
  echo "No area set provided. Please pass a number between 1 and 5."
  exit 1
fi

# Log start time
echo "Starting Seattle Cars scraper for area set $1 at $(date)" >> $LOG_FILE

# Run the Python script, passing the area set as an argument
python3 clBot/seattle_cars.py "$1" >> $LOG_FILE 2>&1

# Check the exit status of the Python script
if [ $? -eq 0 ]; then
  echo "Seattle Cars scraper for area set $1 finished successfully at $(date)" >> $LOG_FILE
else
  echo "Seattle Cars scraper for area set $1 encountered an error at $(date)" >> $LOG_FILE
fi
