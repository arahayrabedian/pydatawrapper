import hashlib
import httplib
import hmac
import json
import logging
import requests
import urlparse

from helpers import generate_url
from helpers import d

logger = logging.getLogger('request_logger')

DATAWRAPPER_API_PREFIX = ('api',)


class RequestObject(object):
    def make_request(self, method, url, data=None):
        d('%s request: %s' % (method, url))
        response = requests.request(method=method, url=url, data=data)

        d("status code: %s" % response.status_code)
        response.raise_for_status()

        parsed_response = self._parse_response(response)

        return parsed_response  # if any other info like headers are required
                                # a subclass can override the parsed_response
                                # method and make it happen

    def _get_url(self):
        raise NotImplementedError("Each object representing a resource should "
                                  "know it's own URL")

    def _parse_response(self, response=None):
        success = (response.status_code in [httplib.OK, httplib.CREATED] and
                   response.pop("status", None) == 'ok')
        data = json.loads(response.content).pop("data")

        return success, data


# class DatawrapperRequestObject(RequestObject):
#     path = DATAWRAPPER_API_PREFIX
#
#     def __init__(self, session, path=None):
#         self.session = session
#         if path:
#             self.path = path
#
#     def _make_authenticated_request(self, method, url):
#         raise NotImplementedError()
#
#     def _get_url(self):
#         return generate_url(self.session.base_url, self.path)


class Session(RequestObject):
    auth_path = DATAWRAPPER_API_PREFIX + ('auth',)

    def __init__(self, base_url, email, password):
        self.base_url = base_url
        self.email = email
        self.password = password
        self.server_salt = None

    def _get_url(self):
        # special case where we don't get final url from _get_url, beuh.
        return generate_url(self.base_url, self.auth_path)

    def _get_url_for_action(self, action):
        return '/'.join([self._get_url(), action])

    def get_server_salt(self):
        success, data = self.make_request('GET', self._get_url_for_action('salt'))
        if 'salt' in data:
            return data['salt']

    def get_session(self):
        salt = self.get_server_salt()
        hashed_password = self._gen_password_hash(salt, self.password)
        auth_data = {'keeplogin': True,
                     'pwhash': hashed_password,
                     'email': self.email}
        ok, data = self.make_request('POST',
                                     self._get_url_for_action('login'),
                                     data=auth_data)
        print str(data)

    def _gen_password_hash(self, salt, password):
        return hmac.new(salt, msg=password, digestmod=hashlib.sha256).digest().encode('hex')


class SerializableObject(object):

    def to_dict(self):
        raise NotImplementedError()

    def to_json(self):
        json.dumps(self.to_dict())
