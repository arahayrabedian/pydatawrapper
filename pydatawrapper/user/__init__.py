from pydatawrapper.common import DatawrapperRequestObject
from pydatawrapper.common import SerializableObject


LOGIN_URL = '/auth/login'
LOGOUT_URL = '/auth/logout'
SALT_URL = '/auth/salt'


class User(DatawrapperRequestObject, SerializableObject):
    id = None

    def to_dict(self):
        return {}