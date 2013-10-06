# -.- coding: UTF-8 -.-

from flask import redirect, url_for, request, render_template, flash, send_from_directory, g
from app import app
from app.forms import LoginForm
from app.users import User
from flask.ext.login import login_required, login_user, logout_user, current_user


@app.route('/login', methods=['GET', 'POST'])
def login():
    loginform = LoginForm(request.form)
    if request.method == 'POST' and loginform.validate():
        user = User(name=loginform.username.data, password=loginform.password.data)
        print 'login attempt', user
        if user.active is not False:
            login_user(user)
            return redirect(url_for('index'))
    return render_template('main.html', loginform=loginform)

@app.before_request
def before_request():
    g.user = current_user

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('main.html', title='Today I ...', content='null')

@app.errorhandler(401)
def not_logged_in(error):
    flash('Please log in first')
    return redirect(url_for('login'))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.png',
        mimetype='image/png'
    )
