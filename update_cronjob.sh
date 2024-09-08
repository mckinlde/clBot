#!/bin/bash

# Check if the area set is passed as an argument
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
  echo "Usage: ./update_cronjob.sh <area_set_number> <hour> <minute>"
  exit 1
fi

# Get the area set number, hour, and minute from the arguments
AREA_SET=$1
HOUR=$2
MINUTE=$3

# Define the cronjob entry with the area set and time
CRON_JOB="$MINUTE $HOUR * * * /path/to/run_seattle_cars.sh $AREA_SET"

# Backup existing crontab to avoid data loss
crontab -l > mycron_backup

# Ensure the run_seattle_cars.sh script has executable permissions
chmod +x /path/to/run_seattle_cars.sh

# Check if the cron job already exists
if crontab -l | grep -q "/path/to/run_seattle_cars.sh"; then
  # Update the existing cronjob
  crontab -l | sed "s|/path/to/run_seattle_cars.sh .*|$CRON_JOB|" > mycron
else
  # Add the new cronjob
  (crontab -l; echo "$CRON_JOB") | crontab -
fi

# Install the new cron file
crontab mycron

# Clean up
rm mycron

echo "Cronjob updated successfully with area set $AREA_SET, scheduled at $HOUR:$MINUTE."
