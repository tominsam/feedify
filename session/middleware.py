# http://scratchpad.cmlenz.net/370f3e0d58804d38c3bc14e514272fda/

from base64 import b64decode, b64encode
import hashlib
from time import time
import zlib

from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase
from django.core.exceptions import SuspiciousOperation
from django.utils import simplejson
from django.utils.cache import patch_vary_headers
from django.utils.encoding import force_unicode
from django.utils.http import cookie_date

MAX_COOKIE_SIZE = 4096


class SessionMiddleware(object):

    def process_request(self, request):
        cookie = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        request.session = SessionStore(cookie)

    def process_response(self, request, response):
        try:
            session = request.session
        except AttributeError:
            return response # 404 page, for instance
        if session.deleted:
            response.delete_cookie(settings.SESSION_COOKIE_NAME)
        else:
            if session.accessed:
                patch_vary_headers(response, ('Cookie',))
            if session.modified or settings.SESSION_SAVE_EVERY_REQUEST:
                if session.get_expire_at_browser_close():
                    max_age = None
                    expires = None
                else:
                    max_age = session.get_expiry_age()
                    expires = cookie_date(time() + max_age)
                cookie = session.encode(session._session)
                if len(cookie) <= MAX_COOKIE_SIZE:
                    response.set_cookie(settings.SESSION_COOKIE_NAME, cookie,
                        max_age = max_age, expires=expires,
                        domain = settings.SESSION_COOKIE_DOMAIN,
                        path = settings.SESSION_COOKIE_PATH,
                        secure = settings.SESSION_COOKIE_SECURE or None
                    )
                else:
                    # The data doesn't fit into a cookie, not sure what's the
                    # best thing to do in this case. Right now, we just leave
                    # the old cookie intact if there was one. If Django had
                    # some kind of standard logging interface, we could also
                    # log a warning here.
                    pass
        return response


class SessionStore(SessionBase):

    def __init__(self, cookie):
        SessionBase.__init__(self, 'cookie')
        self.cookie = cookie
        self.deleted = False

    def exists(self, session_key):
        return self.cookie and not self.deleted

    def create(self):
        pass

    def save(self, must_create=False):
        pass

    def delete(self, session_key=None):
        self.deleted = True

    def load(self):
        if self.cookie:
            return self.decode(self.cookie)
        return {}

    def cycle_key(self):
        pass

    def encode(self, session_dict):
        json = simplejson.dumps(session_dict)
        json_md5 = hashlib.md5(json + settings.SECRET_KEY).hexdigest()
        try:
            return b64encode(zlib.compress(json + json_md5))
        except Exception, e:
            return ''

    def decode(self, session_data):
        try:
            data = zlib.decompress(b64decode(session_data))
        except Exception, e:
            return {}
        json, json_md5 = data[:-32], data[-32:]
        if hashlib.md5(json + settings.SECRET_KEY).hexdigest() != json_md5:
            raise SuspiciousOperation('User tampered with session cookie')
        return simplejson.loads(json)
