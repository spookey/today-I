#!./venv/bin/python
# -.- coding: UTF-8 -.-

import os, sys
thisdir = os.path.dirname(os.path.abspath(__file__))

activate_this = os.path.join(thisdir, 'venv/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

sys.path.insert(0, thisdir)

from app import app as application
