import urlparse


def generate_url(base, paths=()):
    parser = urlparse.urljoin(base, '/'.join(paths))
    return parser
