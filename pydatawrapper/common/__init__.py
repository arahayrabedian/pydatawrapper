import json

DATAWRAPPER_API_PREFIX = '/api'

class DatawrapperRequestObject(object):
    pass


class SerializableObject(object):

    def to_dict(self):
        raise NotImplementedError()

    def to_json(self):
        json.dumps(self.to_dict())
