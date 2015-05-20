import urlparse
import logging

logger = logging.getLogger('pydatawrapper')


def generate_url(base, paths=()):
    parser = urlparse.urljoin(base, '/'.join(paths))
    return parser


def d(msg):
    # logger.debug(msg)
    print msg