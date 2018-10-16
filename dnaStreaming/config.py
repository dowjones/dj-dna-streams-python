from __future__ import absolute_import, division, print_function

import errno
import json
import os

# Python3 has FileNotFoundError defined. Python2 does not.
from dnaStreaming.services.credentials_service import get_authentication_headers

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


class Config(object):
    OAUTH_URL = 'https://accounts.dowjones.com/oauth2/v1/token'
    DEFAULT_HOST_URI = 'https://api.dowjones.com'

    DEFAULT_CUST_CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), './customer_config.json'))
    ENV_VAR_USER_KEY = 'USER_KEY'
    ENV_VAR_SUBSCRIPTION_ID = 'SUBSCRIPTION_ID'
    ENV_VAR_USER_ID = 'USER_ID'
    ENV_VAR_CLIENT_ID = 'CLIENT_ID'
    ENV_VAR_PASSWORD = 'PASSWORD'
    ENV_VAR_HOST = 'HOST_URI'

    def __init__(self, account_id=None, user_id=None, client_id=None, password=None):
        self.customer_config_path = self.DEFAULT_CUST_CONFIG_PATH
        self.initialized = False
        self.account_id = account_id
        self.user_id = user_id
        self.client_id = client_id
        self.password = password

        self.headers = None

    def _initialize(self):
        self._validate()

        with open(self.customer_config_path, 'r') as f:
            self.customer_config = json.load(f)

        self.initialized = True
        self.headers = None

    def _validate(self):
        if not os.path.isfile(self.customer_config_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.customer_config_path)

        if not os.access(self.customer_config_path, os.R_OK):
            raise Exception('Encountered permission problem reading file from path \'{}\'.'.format(self.customer_config_path))

    def get_headers(self):
        if self.headers:
            return self.headers
        else:
            self.headers = get_authentication_headers(self)
            return self.headers

    def subscription(self):
        if os.getenv(self.ENV_VAR_SUBSCRIPTION_ID) is not None:
            subscription = os.getenv(self.ENV_VAR_SUBSCRIPTION_ID)
        else:
            subscription = self._subscription_id_from_file()

        return subscription

    def _set_customer_config_path(self, path):
        self.customer_config_path = path
        self._initialize()

    def _subscription_id_from_file(self):
        if not self.initialized:
            self._initialize()

        return self.customer_config['subscription_id']