```Bash
cd Downloads
```
# - Now the ssh connection, then one of the below
```Bash
cd clBot/
git stash
git pull origin main
cd ../
pkill Xvfb
Xvfb :99 -screen 0 1024x768x16 &  # Start Xvfb in the background
export DISPLAY=:99  # Set the DISPLAY environment variable
nohup python3 clBot/seattle_cars.py 1 > seattle_cars.log 2>&1 &
```
```Bash
cd clBot/
git stash
git pull origin main
cd ../
pkill Xvfb
Xvfb :99 -screen 0 1024x768x16 &  # Start Xvfb in the background
export DISPLAY=:99  # Set the DISPLAY environment variable
nohup python3 clBot/seattle_cars.py 1 > seattle_cars.log 2>&1 &
```
```Bash
cd clBot/
git stash
git pull origin main
cd ../
pkill Xvfb
Xvfb :99 -screen 0 1024x768x16 &  # Start Xvfb in the background
export DISPLAY=:99  # Set the DISPLAY environment variable
nohup python3 clBot/seattle_cars.py 2 > seattle_cars.log 2>&1 &
```
```Bash
cd clBot/
git stash
git pull origin main
cd ../
pkill Xvfb
Xvfb :99 -screen 0 1024x768x16 &  # Start Xvfb in the background
export DISPLAY=:99  # Set the DISPLAY environment variable
nohup python3 clBot/seattle_cars.py 3 > seattle_cars.log 2>&1 &
```
```Bash
cd clBot/
git stash
git pull origin main
cd ../
pkill Xvfb
Xvfb :99 -screen 0 1024x768x16 &  # Start Xvfb in the background
export DISPLAY=:99  # Set the DISPLAY environment variable
nohup python3 clBot/seattle_cars.py 4 > seattle_cars.log 2>&1 &
```
```Bash
cd clBot/
git stash
git pull origin main
cd ../
pkill Xvfb
Xvfb :99 -screen 0 1024x768x16 &  # Start Xvfb in the background
export DISPLAY=:99  # Set the DISPLAY environment variable
nohup python3 clBot/seattle_cars.py 5 > seattle_cars.log 2>&1 &
```
