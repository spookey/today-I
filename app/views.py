# -.- coding: UTF-8 -.-

from flask import redirect, url_for, request, render_template, flash, send_from_directory, g, session
from flask.ext.login import login_required, login_user, logout_user, current_user
from werkzeug import secure_filename
from os import path
from app import app
from log import logger
from config import taskattachments
from app.forms import LoginForm, TaskForm
from app.users import User
from app.store import store


@app.route('/login', methods=['GET', 'POST'])
def login():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = User(name=loginform.username.data, password=loginform.password.data)
        if user.active is not False:
            login_user(user)
            logger.info('logged in %s' %(current_user.name))
            return redirect(url_for('index'))
    if current_user.is_authenticated():
        logger.info('already logged in %s' %(current_user))
        return redirect(url_for('index'))
    return render_template('main.html', title='Today I logged in...', loginform=loginform)

@app.before_request
def before_request():
    g.user = current_user

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logger.info('logged out %s' %(current_user.name))
    logout_user()
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    taskform = TaskForm()
    if taskform.validate_on_submit():
        description = None
        filename = None
        if taskform.description.data:
            description = taskform.description.data
        if taskform.image.data:
            filename = secure_filename(taskform.image.data.filename)
            taskform.image.data.save(path.join(taskattachments, filename))
        store(description, filename)
    return render_template('main.html', title='Today I ...', taskform=taskform)


@app.errorhandler(401)
def not_logged_in(error):
    flash('Please log in first')
    logger.info('redirected to login')
    return redirect(url_for('login'))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.png',
        mimetype='image/png'
    )
