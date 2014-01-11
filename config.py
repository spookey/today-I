# -.- coding: UTF-8 -.-

from os import path

basedir = path.abspath(path.dirname(__file__))

# logging
logdir = path.join(basedir, 'logs')
logfile = path.join(logdir, 'logfile.log')

# tasks
taskdir = path.join(basedir, 'tasks')
taskjson = path.join(taskdir, 'current.json')
taskattachdir = path.join(taskdir, 'images')

# task archives (in subfolders by date)
taskarchive = path.join(taskdir, 'archive')
taskarchivejson_name = 'current.json'

# allowed extensions for upload
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif']

#>>> import os
#>>> os.urandom(24)
SECRET_KEY = 'Set your secret key for flask here!'

# LDAP login
LDAPserver = 'ldap.awesome-server.com'
LDAPPort = 636
LDAPbasedn = 'ou=users,dc=awesome,dc=de'
LDAPinactivegid = 1337

# Wordpress login
WPxmlrpc = 'http://your.awesome-blog.com/xmlrpc.php'
WPuser = 'user'
WPpass = 'pass'

# Wordpress Post Template
pskel = u'<dt>{user}:</dt>\n<dd>{image}<i>{description}</i></dd>\n'
iskel = u'<img src="{imageurl}" alt="{imagealt}"><br />\n'

report_headline = u'Weekly Report'
post_tag = ['awesome']
category = ['Awesome Posts']
