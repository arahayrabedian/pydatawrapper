from pydatawrapper.common import DATAWRAPPER_API_PREFIX
from pydatawrapper.common import DatawrapperRequestObject
from pydatawrapper.common import MappableFieldsObject


CHART_URLS = {
    'GET': '/charts',
    'POST': '/charts/%(id)s',
    'PUT': '/charts/%(id)s',
}

GALLERY_URLS = {
    'GET': '/gallery/',
}


class Data(DatawrapperRequestObject):
    transpose = False
    horizontal_header = True
    vertical_header = True
    source = None

    field_mapping = {
        'horizontal_header': 'horizontal-header',
        'vertical_header': 'vertical-header',
    }

    def to_dict(self):
        return {
            'transpose': self.transpose,
            'horizontal-header': self.horizontal_header,
            'vertical-header': self.vertical_header,
            'source': self.source,
        }


class Visualize(MappableFieldsObject):
    highlighted_series = []
    show_total = False
    selected_row = 0

    def to_dict(self):
        return {
            'highlighted-series': self.highlighted_series,
            'show-total': self.show_total,
            'selected-row': self.selected_row,
        }


class Describe(MappableFieldsObject):
    source_name = None
    source_url = None
    number_format = "n2"
    number_divisor = "0"
    number_currency = "USD|\u0024"
    number_unit = ""

    def to_dict(self):
        return {
            'source-name': self.source_name,
            'source-url': self.source_url,
            'number-format': self.number_format,
            'number-divisor': self.number_divisor,
            'number-currency': self.number_currency,
            'number-unit': self.number_unit,
        }


class Publish(MappableFieldsObject):
    embed_height = 600
    embed_width = 400

    def to_dict(self):
        return {
            'embed-width': self.embed_width,
            'embed-height': self.embed_height
        }


class Chart(DatawrapperRequestObject):
    """ Our representation of the Chart resource, it _MUST_ be instantiated
    with a valid and logged in user, this is so that API requests are
    authenticated
    """
    path = DATAWRAPPER_API_PREFIX + ('charts',)
    field_mapping = {
        'author_id': 'authorId',
        'last_modified_at': 'lastModifiedAt',
        'created_at': 'createdAt',
        'public_url': 'publicUrl',
        'show_in_gallery': 'showInGallery',
    }

    id = None
    title = None
    theme = None
    chart_type = None
    author_id = None
    show_in_gallery = False
    language = 'en'
    created_at = None
    last_modified_at = None
    public_url = None
    metadata = {}

    def __init__(self, session, id):
        super(Chart, self).__init__(session, path=self.path)

        # add id to the path
        assert id is not None
        self.id = id
        self.path += (id,)

        self.metadata = {
            'data': Data(self.session),
            'visualize': Visualize(),
            'describe': Describe(),
            'publish': Publish(),
        }

    def to_dict(self):
        """ Serializes the current Chart, in order to prepare for API usage.
        limited documentation available at:
        https://github.com/datawrapper/datawrapper/wiki/API-Documentation

        :return: the data serialized in a format the API can understand
        """
        pass
