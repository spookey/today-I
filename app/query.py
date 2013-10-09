# -.- coding: UTF-8 -.-

import os, time, json
from datetime import datetime
from log import logger


def format_timestamp(value):
    if isinstance(value, float):
        return datetime.fromtimestamp(value).strftime('%a %d.%m - %H:%M')

def readjson(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                return json.loads(f.read())
            except Exception as e:
                logger.warning('could not unpack: %s' %(e))
