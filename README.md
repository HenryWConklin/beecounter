Dashboard and arduino code for an IOT bee counter device.

# Installation

```
git clone git@github.com:HenryWConklin/beecounter.git
cd beecounter
pip install -r requirements.txt
```

# Running
```
# Listen for detections from the IoT device
python listener.py
# Host the front-end dashboard
python dashboard.py
```

# Files

beeCounter.ino: Arduino sketch code for NodeMCU development board for ESP8266

dashboard.py: Dashboard code, do `python dashboard.py` to start the dashboard server

deploy.wsgi: WSGI entrypoint if you want to run this on a real webserver like Apache or nginx

bees.db: Sample database

listener.py: Listener server, listens for pings from the IOT device and saves them to the databse
