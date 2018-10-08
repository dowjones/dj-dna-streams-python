from __future__ import absolute_import, division, print_function

import errno
import json
import os

# Python3 has FileNotFoundError defined. Python2 does not.
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


class Config(object):
    OAUTH_URL = 'https://accounts.dowjones.com/oauth2/v1/token'
    CRED_ALPHA_PROD_URI = 'https://api.dowjones.com/alpha/accounts/streaming-credentials'
    CRED_DNA_PROD_URI = 'https://api.dowjones.com/dna/accounts/streaming-credentials'

    DEFAULT_CUST_CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), './customer_config.json'))
    ENV_VAR_SERVICE_ACCOUNT_ID = 'SERVICE_ACCOUNT_ID'
    ENV_VAR_SUBSCRIPTION_ID = 'SUBSCRIPTION_ID'
    ENV_VAR_CREDENTIALS_URI = 'CREDENTIALS_URI'
    ENV_VAR_STREAMS_URI = 'STREAMS_URI'
    ENV_VAR_USER_ID = 'USER_ID'
    ENV_VAR_CLIENT_ID = 'CLIENT_ID'
    ENV_VAR_PASSWORD = 'PASSWORD'

    def __init__(self, account_id=None, user_id=None, client_id=None, password=None):
        self.customer_config_path = self.DEFAULT_CUST_CONFIG_PATH
        self.initialized = False
        self.account_id = account_id
        self.user_id = user_id
        self.client_id = client_id
        self.password = password

    def _initialize(self):
        self._validate()

        with open(self.customer_config_path, 'r') as f:
            self.customer_config = json.load(f)

        self.initialized = True

    def _validate(self):
        if not os.path.isfile(self.customer_config_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.customer_config_path)

        if not os.access(self.customer_config_path, os.R_OK):
            raise Exception('Encountered permission problem reading file from path \'{}\'.'.format(self.customer_config_path))

    # return credentials (user_id, client_id, and password) for obtaining a JWT via OAuth2 if all these fields are defined in the constructor, env vars or config file
    # otherwise return None (the client will have to authenticate Extraction API request with an account ID, i.e. the old way)
    def oauth2_credentials(self):
        creds = self._build_oauth2_credentials(
            self.user_id,
            self.client_id,
            self.password
        )
        if not creds:
            creds = self._build_oauth2_credentials(
                os.getenv(self.ENV_VAR_USER_ID),
                os.getenv(self.ENV_VAR_CLIENT_ID),
                os.getenv(self.ENV_VAR_PASSWORD)
            )
        if not creds:
            creds = self._oauth2_credentials_from_file()
        return creds

    def _oauth2_credentials_from_file(self):
        if not self.initialized:
            self._initialize()

        return self._build_oauth2_credentials(
            self.customer_config.get('user_id'),
            self.customer_config.get('client_id'),
            self.customer_config.get('password')
        )

    def _build_oauth2_credentials(self, user_id, client_id, password):
        if user_id and client_id and password:
            return {
                'user_id': user_id,
                'client_id': client_id,
                'password': password
            }
        return None

    def service_account_id(self):
        if self.account_id is not None:
            service_account_id = self.account_id
        else:
            service_account_id = os.getenv(self.ENV_VAR_SERVICE_ACCOUNT_ID)

            if service_account_id is None:
                service_account_id = self._service_account_id_from_file()

        return service_account_id

    def _service_account_id_from_file(self):
        if not self.initialized:
            self._initialize()

        return self.customer_config.get('service_account_id')

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

    def credentials_uri(self, headers):
        if 'Authorization' in headers:
            return os.getenv(self.ENV_VAR_CREDENTIALS_URI, self.CRED_DNA_PROD_URI)
        else:
            return os.getenv(self.ENV_VAR_CREDENTIALS_URI, self.CRED_ALPHA_PROD_URI)
