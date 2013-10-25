# -.- coding: UTF-8 -.-

import os, time, json
from datetime import datetime
from log import logger
from config import taskjson
from flask.ext.login import current_user
from app.query import readjson
from htmlentitydefs import codepoint2name

def writejson(filename, data):
    with open(filename, 'w') as f:
        try:
            f.write(json.dumps(data, indent=2, encoding='utf-8'))
            logger.info('packed %d values' %(len(data)))
        except Exception as e:
            logger.warning('could not pack: %s' %(e))


def store(description, image):

    def _strconv(msg):
        htmlentities = list()
        for c in msg:
            if ord(c) in codepoint2name:
                htmlentities.append('&%s;' % codepoint2name[ord(c)])
            else:
                htmlentities.append(c)
        return ''.join(htmlentities)

    plus = {
        'timestamp': time.time(),
        'data': {
            'user': current_user.name,
            'description': _strconv(description).encode('utf-8'),
            'image': image,
            },
        }

    data = readjson(taskjson)

    if data is None:
        data = []

    data.append(plus)

    writejson(taskjson, data)
    logger.info('new entry from %s: %s image: %s' %(current_user.name, description, image))

