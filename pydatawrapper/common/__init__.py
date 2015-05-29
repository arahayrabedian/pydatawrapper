import hashlib
import httplib
import hmac
import json
import requests

from helpers import generate_url

DATAWRAPPER_API_PREFIX = ('api',)


class RequestObject(object):
    def make_request(self, method, url, headers=None, cookies=None, data=None):
        print('%s request: %s' % (method, url))
        response = requests.request(method=method,
                                    url=url,
                                    data=data,
                                    headers=headers,
                                    cookies=cookies)

        print("status code: %s: %s" % (response.status_code, response.content))
        response.raise_for_status()

        parsed_response = self._parse_response(response)

        return parsed_response

    def _get_url(self):
        raise NotImplementedError("Each object representing a resource should "
                                  "know it's own URL")

    def _parse_response(self, response):
        success = response.status_code in [httplib.OK, httplib.CREATED]
        full_data = json.loads(response.content)

        success = success and full_data.pop("status", None) == 'ok'
        data = full_data.get('data', None)

        return success, data, response


# class DatawrapperRequestObject(RequestObject):
#     path = DATAWRAPPER_API_PREFIX
#
#     def __init__(self, session, path=None):
#         self.session = session
#         if path:
#             self.path = path
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
        self.session_key = None

    def _get_url(self):
        # special case where we don't get final url from _get_url, beuh.
        return generate_url(self.base_url, self.auth_path)

    def _get_url_for_action(self, action):
        return '/'.join([self._get_url(), action])

    def _gen_password_hash(self, salt, password):
        return hmac.new(salt, msg=password, digestmod=hashlib.sha256).digest().encode('hex')

    def get_server_salt(self):
        success, data, response = self.make_request('GET', self._get_url_for_action('salt'))
        if 'salt' in data:
            return str(data['salt'])

    def get_session(self):
        salt = self.get_server_salt()
        hashed_password = self._gen_password_hash(salt, self.password)
        auth_data = {
            'keeplogin': 'true',
            'pwhash': hashed_password,
            'email': self.email
        }
        ok, data, response = self.make_request('POST',
                                              self._get_url_for_action('login'),
                                              data=json.dumps(auth_data))
        # TODO: check status as well because apparently we get a session whether or not we have a valid session
        if 'DW-SESSION' in response.cookies:
            self.session_key = response.cookies['DW-SESSION']
            return self.session_key
        else:
            return None

    def make_authenticated_request(self, method, url):
        assert self.session_key is not None
        headers = {
            'accepts': 'application/json',
        }
        cookies = {
            'DW-SESSION': self.session_key,
        }
        self.make_request(method=method, url=url, headers=headers,
                          cookies=cookies)


class SerializableObject(object):

    def to_dict(self):
        raise NotImplementedError()

    def to_json(self):
        json.dumps(self.to_dict())
