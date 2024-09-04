#!/bin/bash

# Update the package list
sudo yum update -y

# Install dependencies
sudo yum install -y wget unzip curl
sudo yum install -y fontconfig freetype freetype-devel alsa-lib atk cairo \
    cups-libs dbus-glib GConf2 libX11 libXcomposite libXcursor libXdamage \
    libXext libXi libXrandr libXScrnSaver libXtst pango

# Remove any existing Chrome installation
sudo yum remove -y google-chrome-stable

# Download and install the latest stable version of Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
sudo yum install -y ./google-chrome-stable_current_x86_64.rpm

# Verify Chrome installation
google-chrome --version

# Download the latest stable version of ChromeDriver from the new source
wget -N https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/115.0.5790.170/linux64/chromedriver-linux64.zip

# Unzip and move ChromeDriver to /usr/local/bin
unzip chromedriver-linux64.zip
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver

# Clean up
rm -rf chromedriver-linux64.zip chromedriver-linux64

# Install pip and Selenium
sudo yum install -y python3-pip
pip3 install selenium

# Create a sample Python script to test headless Chrome
cat <<EOL > selenium_test.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up ChromeDriver
service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Example test
driver.get("http://www.google.com")
print(driver.title)

driver.quit()
EOL

# Run the Selenium test
python3 selenium_test.py
