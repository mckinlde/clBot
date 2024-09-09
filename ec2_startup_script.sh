cd Downloads
cd clBot/
git stash
git pull origin main
cd ../
pkill Xvfb
Xvfb :99 -screen 0 1024x768x16 &  # Start Xvfb in the background
export DISPLAY=:99  # Set the DISPLAY environment variable
nohup python3 clBot/seattle_cars.py 1 > seattle_cars.log 2>&1 &
