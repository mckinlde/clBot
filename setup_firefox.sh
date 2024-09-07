wget "https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US" -O firefox-latest.tar.bz2
tar xjf firefox-latest.tar.bz2
sudo mv firefox /opt/firefox
sudo ln -s /opt/firefox/firefox /usr/local/bin/firefox
firefox --version
firefox --headless --screenshot https://www.google.com
