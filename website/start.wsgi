import os, sys

PROJECT_DIR = '/home/skylerroh/w209'

activate_this = '/home/skylerroh/w209/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

sys.path.append(PROJECT_DIR)

from routes import app as application
