from __future__ import absolute_import, division

import errno
import json
import os
import requests

class Config(object):
    OAUTH_URL = 'https://accounts.dowjones.com/oauth2/v1/token'
    DEFAULT_HOST = 'https://api.dowjones.com'

    DEFAULT_CUST_CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), './customer_config.json'))
    ENV_VAR_SUBSCRIPTION_ID = 'SUBSCRIPTION_ID'
    ENV_VAR_USER_KEY = 'USER_KEY'
    ENV_VAR_SERVICE_ACCOUNT_ID = 'SERVICE_ACCOUNT_ID'
    ENV_VAR_USER_ID = 'USER_ID'
    ENV_VAR_CLIENT_ID = 'CLIENT_ID'
    ENV_VAR_PASSWORD = 'PASSWORD'
    ENV_VAR_API_HOST = 'API_HOST'

    def __init__(self, service_account_id=None, user_key=None, user_id=None, client_id=None, password=None):
        self.customer_config_path = self.DEFAULT_CUST_CONFIG_PATH
        self.initialized = False
        self.service_account_id = service_account_id
        self.user_key = user_key
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
            self.headers = self.get_authentication_headers()
            return self.headers

    def get_authentication_headers(self):
        if self.oauth2_credentials():
            return {
                'Authorization': self._fetch_jwt()
            }

        # missing oauth creds, authenticate the old way via user key
        user_key = self.get_user_key()
        if user_key:
            return {
                'user-key': user_key
            }

        else:
            msg = '''Could not find determine credentials:
                Must specify account credentials as user_id, client_id, and password, either through env vars, customer_config.json, or as args to Listener constructor
                (see README.rst)'''
            raise Exception(msg)

    def _fetch_jwt(self):
        oauth2_credentials = self.oauth2_credentials()
        user_id = oauth2_credentials.get('user_id')
        client_id = oauth2_credentials.get('client_id')
        password = oauth2_credentials.get('password')

        # two requests need to be made, to the same URL, with slightly different params, to finally obtain a JWT
        # the second request contains params returned in the response of the first request
        # I know this makes no sense but it is what it is
        body = {
            'username': user_id,
            'client_id': client_id,
            'password': password,
            'connection': 'service-account',
            'grant_type': 'password',
            'scope': 'openid service_account_id'
        }

        try:

            response = _get_requests().post(self.OAUTH_URL, data=body).json()
            body['scope'] = 'openid pib'
            body['grant_type'] = 'urn:ietf:params:oauth:grant-type:jwt-bearer'
            body['access_token'] = response.get('access_token')
            body['assertion'] = response.get('id_token')

            response = _get_requests().post(self.OAUTH_URL, data=body).json()

            return '{0} {1}'.format(response['token_type'], response['access_token'])
        except (KeyError, ValueError):
            msg = '''Unable to retrieve JWT with the given credentials:
                User ID: {0}
                Client ID: {1}
                Password: {2}
            '''.format(user_id, client_id, password)
            raise Exception(msg)

    def get_uri_context(self):
        headers = self.get_headers()
        host = os.getenv(self.ENV_VAR_API_HOST, self.DEFAULT_HOST)
        if "Authorization" in headers:
            return host + '/dna'
        elif 'user-key' in headers:
            return host + '/alpha'
        else:
            msg = '''Could not determine user credentials:
                Must specify account credentials as user_id, client_id, and password, either through env vars, customer_config.json, or as args to Listener constructor
                (see README.rst)'''
            raise Exception(msg)

    # return credentials (user_id, client_id, and password) for obtaining a JWT via OAuth2 if all these fields are defined in the constructor, env vars or config file
    # otherwise return None (the client will have to authenticate API request with an user key, i.e. the original standard)
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


def _get_requests():
    return requests
