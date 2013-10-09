#!./venv/bin/python
# -.- coding: UTF-8 -.-

activate_this = '/srv/today-i/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, '/srv/today-i/')

from app import app as application
