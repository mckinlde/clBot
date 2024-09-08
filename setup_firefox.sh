wget "https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US" -O firefox-latest.tar.bz2
tar xjf firefox-latest.tar.bz2
sudo mv firefox /opt/firefox
sudo ln -s /opt/firefox/firefox /usr/local/bin/firefox
sudo yum install -y mesa-libGL
export MOZ_HEADLESS=1
sudo yum install -y xorg-x11-server-Xvfb
Xvfb :99 & export DISPLAY=:99
firefox --version
firefox --headless --screenshot https://www.google.com
