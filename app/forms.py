# -.- coding: UTF-8 -.-

from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import TextField, PasswordField, SubmitField, HiddenField, TextAreaField, validators
from config import ALLOWED_EXTENSIONS

class LoginForm(Form):
    username = TextField('Username', validators=[validators.Length(min=2, message=u'Mindestens zwei Zeichen benötigt'), validators.Required(message='Der Name muss dabei sein.')], description='LDAP Login Name')
    password = PasswordField('Password', validators=[validators.Required(message='Ohne Password kein Login')], description='Passwort')
    submit = SubmitField('Login')

class TaskForm(Form):
    description = TextAreaField('Beschreibung', validators=[validators.Length(min=3, message='Wenigstens drei Zeichen solltest du schon schreiben..')], description='Heute habe ich...')
    image = FileField('image', validators=[FileAllowed(ALLOWED_EXTENSIONS, 'Nur Bilder sind erlaubt (%s)!!1!' %(ALLOWED_EXTENSIONS))])
    submit = SubmitField('Los')
