import os
import sys
import site

# Add virtualenv site packages
site.addsitedir(os.path.join(os.path.dirname(__file__),     'venv/local/lib/python3.6/site-packages'))

# Path of execution
sys.path.append('/home/ec2-user/beecounter-dash')
sys.path.append('/home/ec2-user/beecounter-dash/venv/local/lib/python3.6/site-packages')

# import my_flask_app as application
from dashboard import app as application
