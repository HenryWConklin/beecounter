import os
import sys
import site

# Path of execution
sys.path.append('/home/ec2-user/beecounter-dash')

# import my_flask_app as application
from dashboard import app 
application = app.server
