import os
import sys
import site

# Add virtualenv site packages
site.addsitedir(os.path.join(os.path.dirname(__file__),     'venv/local/lib64/python3.6/site-packages'))

# Path of execution
sys.path.append('/home/ec2-user/beecounter-dash')

# Fired up virtualenv before include application
activate_env = os.path.expanduser(os.path.join(os.path.dirname(__file__), 'venv/bin/activate_this.py'))
execfile(activate_env, dict(__file__=activate_env))

# import my_flask_app as application
from dashboard import app as application
