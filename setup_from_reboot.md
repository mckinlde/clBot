Once your EC2 instances are rebooted, you can follow these steps to set them up correctly for running your headless Firefox and `seattle_cars.py` script using Selenium with Xvfb. Here's a general step-by-step guide:

### Step 1: Reconnect to Your EC2 Instance
After rebooting the instance, SSH back into it:

```bash
ssh -i /path/to/your-key.pem ec2-user@your-instance-public-ip
```

### Step 2: Install Necessary Dependencies (if not already installed)
Ensure all the required dependencies (like Firefox, Geckodriver, Xvfb, and others) are installed. If these dependencies are not already present, run the following commands:

```bash
sudo yum update -y  # Update all packages

# Install necessary dependencies for Firefox and Selenium
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
    xorg-x11-server-Xvfb \
    wget \
    bzip2

# Download and install the latest Firefox
wget "https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US" -O firefox-latest.tar.bz2
tar xjf firefox-latest.tar.bz2
sudo mv firefox /opt/firefox
sudo ln -s /opt/firefox/firefox /usr/local/bin/firefox

# Download and set up Geckodriver
wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz
tar -xvzf geckodriver-v0.33.0-linux64.tar.gz
sudo mv geckodriver /usr/local/bin/
sudo chmod +x /usr/local/bin/geckodriver
```

### Step 3: Start Xvfb
Xvfb is necessary to run headless Firefox. Start Xvfb on display `:99` and export the `DISPLAY` environment variable:

```bash
Xvfb :99 -screen 0 1024x768x16 &
export DISPLAY=:99
```

If you receive a lock file error, make sure to remove the lock first:

```bash
rm /tmp/.X99-lock
Xvfb :99 -screen 0 1024x768x16 &
export DISPLAY=:99
```

### Step 4: Verify Firefox and Geckodriver Installation
Run the following commands to verify that both Firefox and Geckodriver are installed and set up correctly:

```bash
firefox --version
geckodriver --version
```

### Step 5: Configure the Cronjob
Ensure that your cronjobs are correctly set up to run the script. Use the `update_cronjob.sh` script you created to install the cronjob for each instance with the appropriate area set and time:

```bash
./clBot/update_cronjob.sh <area_set_number> <hour> <minute>
```

### Step 6: Run `seattle_cars.py`
To verify that the setup is working, manually run the script:

```bash
python3 clBot/seattle_cars.py
```

### Step 7: Monitor Logs
Check the logs to make sure the script is running smoothly. You can check the log file created by the script:

```bash
tail -f /home/ec2-user/seattle_cars_error.log
```

### Additional Considerations
- **Autostart on Reboot**: If you want Xvfb to start automatically after a reboot, you can add the Xvfb command to your crontab or `/etc/rc.local` file.
- **Debugging**: If the script hangs, check the logs for any errors related to the driver or Xvfb setup.
