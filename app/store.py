# -.- coding: UTF-8 -.-

import os, time, json
from datetime import datetime
from log import logger
from config import taskjson
from flask.ext.login import current_user
from app.query import readjson

def writejson(filename, data):
    with open(filename, 'w') as f:
        try:
            f.write(json.dumps(data, indent=2))
            logger.info('packed %d values' %(len(data)))
        except Exception as e:
            logger.warning('could not pack: %s' %(e))


def store(description, image):

    plus = {
        'timestamp': time.time(),
        'data': {
            'user': current_user.name,
            'description': description,
            'image': image,
            },
        }

    data = readjson(taskjson)

    if data is None:
        data = []

    data.append(plus)

    writejson(taskjson, data)
    logger.info('new entry from %s: %s image: %s' %(current_user.name, description, image))

