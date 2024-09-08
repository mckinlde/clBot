#!/bin/bash

# Download and extract Firefox
wget "https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US" -O firefox-latest.tar.bz2
tar xjf firefox-latest.tar.bz2

# Move Firefox to /opt and create a symlink
sudo mv firefox /opt/firefox || { echo "Failed to move Firefox to /opt"; exit 1; }
sudo ln -sf /opt/firefox/firefox /usr/local/bin/firefox || { echo "Failed to create Firefox symlink"; exit 1; }

# Install necessary libraries
sudo yum install -y mesa-libGL mesa-libEGL xorg-x11-server-Xvfb libXrender libXcomposite libXcursor libXi libXtst alsa-lib || { echo "Failed to install required libraries"; exit 1; }

sudo yum install -y \
    dbus-glib \
    libXt \
    mesa-libEGL \
    mesa-libGL \
    alsa-lib \
    atk \
    cups-libs \
    gtk3 \
    libXcomposite \
    libXcursor \
    libXdamage \
    libXrandr \
    xorg-x11-server-Xvfb

# Set up headless mode with Xvfb
export MOZ_HEADLESS=1
Xvfb :99 -screen 0 1024x768x16 &  # Start Xvfb in the background
export DISPLAY=:99  # Set the DISPLAY environment variable


# Download and set up Geckodriver
wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz
tar -xvzf geckodriver-v0.33.0-linux64.tar.gz
sudo mv geckodriver /usr/local/bin/ || { echo "Failed to move Geckodriver"; exit 1; }

# Check Firefox and Geckodriver installation
firefox --version || { echo "Firefox is not installed correctly"; exit 1; }
geckodriver --version || { echo "Geckodriver is not installed correctly"; exit 1; }

# Run a test with Firefox in headless mode
firefox --headless --screenshot https://www.google.com || { echo "Failed to run Firefox in headless mode"; exit 1; }

# Output success message
echo "Firefox and Geckodriver setup complete."

# from ec2-user% you can run this with:
# cd clBot/
# git pull origin main
# cd ../
# chmod +x ~/clBot/setup_firefox.sh
# ./clBot/setup_firefox.sh
