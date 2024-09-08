#!/bin/bash

# Check if the area set is passed as an argument
if [ -z "$1" ]; then
  echo "Usage: ./update_cronjob.sh <area_set_number>"
  exit 1
fi

# Get the area set number from the argument
AREA_SET=$1

# Define the cronjob entry with the area set
CRON_JOB="0 0 * * * /path/to/run_seattle_cars.sh $AREA_SET"

# Backup existing crontab to avoid data loss
crontab -l > mycron_backup

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

echo "Cronjob updated successfully with area set $AREA_SET."
