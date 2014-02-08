# -.- coding: UTF-8 -.-

from config import LDAPserver, LDAPPort, LDAPbasedn, LDAPinactivegid, LDAPtest
from flask.ext.login import LoginManager, UserMixin
from app import login_manager
from log import logger
if not LDAPtest:
    from simpleldap import Connection

def ldap_fetch(uid=None, name=None, password=None):
    try:
        if name is not None and password is not None:
            l = Connection(LDAPserver, port=LDAPPort, encryption='ssl', dn='uid=%s,%s' %(name, LDAPbasedn), password=password)
            r = l.search('uid=%s' %(name), base_dn=LDAPbasedn)
        else:
            l = Connection(LDAPserver, port=LDAPPort, encryption='ssl')
            r = l.search('uidNumber=%s' %(uid), base_dn=LDAPbasedn)
        return {
            'name': r[0]['uid'][0],
            'id': unicode(r[0]['uidnumber'][0]),
            'gid': int(r[0]['gidnumber'][0])
        }
    except Exception as e:
        logger.error('can\'t contact LDAP Server: %s' %(e))
        return None

class User(UserMixin):
    def __init__(self, uid=None, name=None, password=None):

        self.active = False

        if LDAPtest is True:
            ldapressource = {'name': 'tester', 'id': u'123', 'gid': 123}
        else:
            ldapressource = ldap_fetch(uid=uid, name=name, password=password)


        if ldapressource is not None:
            self.name = ldapressource['name']
            self.id = ldapressource['id']
            if ldapressource['gid'] != LDAPinactivegid:
                self.active = True
            else:
                logger.warn('inactive user tried to login: %s' %(ldapressource['name']))
            self.gid = ldapressource['gid']

        def is_active(self):
            return self.active

        def get_id(self):
            return self.id

@login_manager.user_loader
def load_user(userid):
    return User(uid=userid)
