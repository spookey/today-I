# -.- coding: UTF-8 -.-

activate_this = '/srv/today-i/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, '/srv/today-i/')

import os, time
from shutil import copy
from datetime import datetime
from app.query import readjson
from app.store import writejson
from mimetypes import guess_type
from config import taskjson, taskattachdir, taskarchive, taskarchivejson, WPxmlrpc, WPuser, WPpass
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media
from wordpress_xmlrpc.methods.posts import NewPost

def folder_timestamp():
    return datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')

archivedir = os.path.join(taskarchive, folder_timestamp())

def backup():
    recent = readjson(taskjson)
    if recent is not None:
        if not os.path.exists(archivedir):
            os.makedirs(archivedir)

        writejson(os.path.join(archivedir, taskarchivejson), recent)

        for element in recent:
            if element['data']['image'] is not None:
                copy(os.path.join(taskattachdir, element['data']['image']), archivedir)

def push():
    recent = readjson(os.path.join(archivedir, taskarchivejson))
    if recent is not None:
        content = '<ul>\n'

        pskel = '<li>{user}:<br />\n{image}<i>{description}</i></li>\n'
        iskel = '<img src="{imageurl}" alt="{imagealt}"><br />\n'

        wp = Client(WPxmlrpc, WPuser, WPpass)

        for element in recent:
            if element['data']['image'] is not None:
                filename = os.path.join(archivedir, element['data']['image'])
                data = {
                    'name': element['data']['image'],
                    'type': guess_type(filename)[0]
                }

                with open(filename, 'rb') as img:
                    data['bits'] = xmlrpc_client.Binary(img.read())

                response = wp.call(media.UploadFile(data))

                content += pskel.format(user=element['data']['user'], image=iskel.format(imageurl=response['url'], imagealt=element['data']['description']), description=element['data']['description'])
            else:
                content += pskel.format(user=element['data']['user'], image='', description=element['data']['description'])

        content += '</ul>\n'

        post = WordPressPost()
        post.title = 'Weekly Report'
        post.content = content
        post.terms_names = {
            'post_tag': ['report'],
            'category': ['Neulich im Space']
        }

        wp.call(NewPost(post))

def delete():
    filelist = [ os.path.join(taskattachdir, f) for f in os.listdir(taskattachdir) if not f.startswith('.') ]
    filelist.append(taskjson)
    for f in filelist:
        if os.path.exists(f):
            os.remove(f)


if __name__ == '__main__':
    backup()
    push()
    delete()
