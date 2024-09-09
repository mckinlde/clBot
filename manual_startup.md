### I'm having way too frusturating of a time using .sh scripts to autostart.

### Why not just manually start one every 20 minutes?

```Bash
crontab -r
cd clBot/
git stash
git pull origin main
cd ../
pkill Xvfb
Xvfb :99 -screen 0 1024x768x16 &  # Start Xvfb in the background
export DISPLAY=:99  # Set the DISPLAY environment variable
```
```Bash
nohup python3 clBot/seattle_cars.py 5 > seattle_cars.log 2>&1 &
```
```Bash
nohup python3 clBot/seattle_cars.py 4 > seattle_cars.log 2>&1 &
```
```Bash
nohup python3 clBot/seattle_cars.py 3 > seattle_cars.log 2>&1 &
```
```Bash
nohup python3 clBot/seattle_cars.py 2 > seattle_cars.log 2>&1 &
```
```Bash
nohup python3 clBot/seattle_cars.py 1 > seattle_cars.log 2>&1 &
```
```Bash
tail -f nohup.out
```
