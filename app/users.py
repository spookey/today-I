# -.- coding: UTF-8 -.-

from config import LDAPserver, LDAPbasedn, LDAPinactivegid
from flask.ext.login import LoginManager, UserMixin
from simpleldap import Connection
from app import login_manager

def ldap_fetch(uid=None, name=None, password=None):
    try:
        if name is not None and password is not None:
            l = Connection(LDAPserver, encryption='ssl', dn='uid=%s,%s' %(name, LDAPbasedn), password=password)
            r = l.search('uid=%s' %(name), base_dn=LDAPbasedn)
        else:
            l = Connection(LDAPserver, encryption='ssl')
            r = l.search('uidNumber=%s' %(uid), base_dn=LDAPbasedn)
        return {
            'name': r[0]['uid'][0],
            'id': unicode(r[0]['uidnumber'][0]),
            'gid': int(r[0]['gidnumber'][0])
        }
    except:
        return None

class User(UserMixin):
    def __init__(self, uid=None, name=None, password=None):

        self.active = False

        ldapressource = ldap_fetch(uid=uid, name=name, password=password)

        if ldapressource is not None:
            self.name = ldapressource['name']
            self.id = ldapressource['id']
            if ldapressource['gid'] != LDAPinactivegid:
                self.active = True
            self.gid = ldapressource['gid']

        def is_active(self):
            return self.active

        def get_id(self):
            return self.id

@login_manager.user_loader
def load_user(userid):
    return User(uid=userid)
