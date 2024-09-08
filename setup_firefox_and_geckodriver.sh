wget "https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US" -O firefox-latest.tar.bz2
tar xjf firefox-latest.tar.bz2
sudo mv firefox /opt/firefox
sudo ln -s /opt/firefox/firefox /usr/local/bin/firefox
sudo yum install -y mesa-libGL
export MOZ_HEADLESS=1
sudo yum install -y xorg-x11-server-Xvfb
Xvfb :99 & export DISPLAY=:99
wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz
tar -xvzf geckodriver-v0.33.0-linux64.tar.gz
sudo mv geckodriver /usr/local/bin/
firefox --version
firefox --headless --screenshot https://www.google.com

# from ec2-user% you can run this with:
# cd clBot/
# git pull origin main
# cd ../
# chmod +x ~/clBot/setup_firefox.sh
# ./clBot/setup_firefox.sh
