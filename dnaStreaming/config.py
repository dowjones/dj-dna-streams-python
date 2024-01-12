from __future__ import absolute_import, division

import errno
import json
import os
from pathlib import Path

class Config(object):

    DEFAULT_HOST = 'https://api.dowjones.com'

    DEFAULT_CUST_CONFIG_PATH = str(Path.home()) + '/customer_config.json'
    ENV_VAR_SUBSCRIPTION_ID = 'SUBSCRIPTION_ID'
    ENV_VAR_USER_KEY = 'USER_KEY'
    ENV_VAR_SERVICE_ACCOUNT_ID = 'SERVICE_ACCOUNT_ID'
    ENV_VAR_API_HOST = 'API_HOST'

    def __init__(self, service_account_id=None, user_key=None, config_file=None):
        self.customer_config_path = self.DEFAULT_CUST_CONFIG_PATH if config_file is None else config_file
        self.initialized = False
        self.service_account_id = service_account_id
        self.user_key = user_key

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
            self.headers = self.get_authentication_headers()
            return self.headers

    def get_authentication_headers(self):

        user_key = self.get_user_key()
        if user_key:
            return {
                'user-key': user_key
            }

        else:
            msg = """
                Unable to find credentials. Specify your account credentials by choosing one of the following ways:
                - set your user key to an env var under the name 'USER_KEY'
                - place your customer_config.json file in your home directory (e.g. ~/, $HOME/)
                - pass the absolute path of your customer_config.json file to the constructor of the Listener class
                - pass the user key as a parameter to the constructor of the Listener class
            """
            raise Exception(msg)

    def get_uri_context(self):
        host = os.getenv(self.ENV_VAR_API_HOST, self.DEFAULT_HOST)
        return host

    # in the following two methods, note that we use "SERVICE_ACCOUNT_ID" as a legacy,
    # alternate name for the "USER_KEY" parameter, from the customer's perspective
    def get_user_key(self):
        user_key = self.user_key if self.user_key else self.service_account_id

        if user_key is None:
            user_key = os.getenv(self.ENV_VAR_USER_KEY,
                                 os.getenv(self.ENV_VAR_SERVICE_ACCOUNT_ID))

            if user_key is None:
                user_key = self._user_key_id_from_file()

        return user_key

    def _user_key_id_from_file(self):
        if not self.initialized:
            self._initialize()

        return self.customer_config.get('user_key',
                                        self.customer_config.get('service_account_id'))

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

