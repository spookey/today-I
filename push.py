# -.- coding: UTF-8 -.-

import os, sys, time

thisdir = os.path.dirname(os.path.abspath(__file__))

activate_this = os.path.join(thisdir, 'venv/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

sys.path.insert(0, thisdir)

from shutil import copy
from datetime import datetime
from app.query import readjson
from app.store import writejson
from log import logger
from mimetypes import guess_type
from config import taskjson, taskattachdir, taskarchive, taskarchivejson, WPxmlrpc, WPuser, WPpass, pskel, iskel
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
        logger.info('backup: %s' %(taskjson))

        for element in recent:
            if element['data']['image'] is not None:
                copy(os.path.join(taskattachdir, element['data']['image']), archivedir)
                logger.info('backup: %s' %(element['data']['image']))
    else:
        logger.info('nothing to backup')

def push():
    recent = readjson(os.path.join(archivedir, taskarchivejson))
    if recent is not None:
        content = '<ul>\n'

        wp = Client(WPxmlrpc, WPuser, WPpass)

        for element in sorted(recent):
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
    else:
        logger.info('nothing to push')

def delete():
    filelist = [ os.path.join(taskattachdir, f) for f in os.listdir(taskattachdir) if not f.startswith('.') ]
    filelist.append(taskjson)
    for f in filelist:
        if os.path.exists(f):
            os.remove(f)
    logger.info('everything\'s gone')


if __name__ == '__main__':
    thisdir = os.path.dirname(os.path.abspath(__file__))

    activate_this = os.path.join(thisdir, 'venv/bin/activate_this.py')
    execfile(activate_this, dict(__file__=activate_this))

    sys.path.insert(0, thisdir)


    logger.info('new push: %s' %(folder_timestamp()))
    backup()
    push()
    delete()
