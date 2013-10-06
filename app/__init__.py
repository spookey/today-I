# -.- coding: UTF-8 -.-

from flask import Flask
app = Flask(__name__)
app.config.from_object('config')

if app.debug is not True:
    from log import filehandler
    app.logger.addHandler(filehandler)
    logger = app.logger

from flask.ext.login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

from app import views
