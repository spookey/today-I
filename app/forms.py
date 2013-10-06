# -.- coding: UTF-8 -.-

from wtforms import Form, TextField, PasswordField, validators

class LoginForm(Form):
    username = TextField('Username', [validators.Length(min=2, max=25)])
    password = PasswordField('Password', [validators.Required()])
