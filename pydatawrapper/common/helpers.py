import logging
import requests


logger = logging.getLogger('request_logger')
GLOBAL_LEGAL_METHODS = ['GET', 'POST', 'PUT']


def make_api_call(method, url):
    if method not in GLOBAL_LEGAL_METHODS:
        raise AttributeError("Only methods allowed are: %s") % str(GLOBAL_LEGAL_METHODS)
    logger.debug('%s request: %s' % (method, url))
    response = requests.request(method=method, url=url)
    logger.log("status code: %s" % response.status_code)
    return response

def make_authenticated_api_call(user, method, url):
    assert user is not None
    pass