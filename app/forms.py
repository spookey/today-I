# -.- coding: UTF-8 -.-

from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import TextField, PasswordField, SubmitField, HiddenField, TextAreaField, validators
from config import ALLOWED_EXTENSIONS

class LoginForm(Form):
    username = TextField('Username', validators=[validators.Length(min=2, message=u'Zu wenig Text..'), validators.Required(message='Der Name muss dabei sein.')], description='LDAP Login Name')
    password = PasswordField('Passwort', validators=[validators.Required(message='Ohne Password kein Login. So einfach ist das.')], description='Passwort')
    submit = SubmitField('Login')

class TaskForm(Form):
    description = TextAreaField('Beschreibung', validators=[validators.Length(min=3, message='Zu wenig Text..')], description='Heute habe ich...')
    image = FileField('Bild', validators=[FileAllowed(ALLOWED_EXTENSIONS, 'Nur Bilder sind erlaubt (%s)!!1!' %(', '.join(ALLOWED_EXTENSIONS)))])
    submit = SubmitField('Los')
