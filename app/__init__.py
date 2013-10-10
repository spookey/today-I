# -.- coding: UTF-8 -.-

from flask import Flask
app = Flask(__name__)
app.config.from_object('config')

if not app.debug:
    from log import filehandler
    import logging
    filehandler.setLevel(logging.INFO)
    app.logger.addHandler(filehandler)

from flask.ext.login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

from flask_wtf.csrf import CsrfProtect
CsrfProtect(app)

from log import logger
notice = 'flask started'
logger.info('\n%s\n%s\n%s' %('=' * len(notice), notice, '=' * len(notice)))

from app import views
