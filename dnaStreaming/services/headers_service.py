from __future__ import absolute_import, division, print_function

import requests


def get_authentication_headers(config):
    if config.oauth2_credentials():
        return {
            'Authorization': _fetch_jwt(config)
        }

    # missing oauth creds, authenticate the old way via account ID
    account_id = config.user_key()
    if account_id:
        return {
            'user-key': account_id
        }

    else:
        msg = '''Could not find determine credentials:
            Must specify account credentials as user_id, client_id, and password, either through env vars, customer_config.json, or as args to Listener constructor
            (see README.rst)'''
        raise Exception(msg)


def _fetch_jwt(config):
    oauth2_credentials = config.oauth2_credentials()
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

    response = _get_requests().post(config.OAUTH_URL, data=body).json()

    body['scope'] = 'openid pib'
    body['grant_type'] = 'urn:ietf:params:oauth:grant-type:jwt-bearer'
    body['access_token'] = response.get('access_token')
    body['assertion'] = response.get('id_token')

    response = _get_requests().post(config.OAUTH_URL, data=body).json()

    try:
        return '{0} {1}'.format(response['token_type'], response['access_token'])
    except KeyError:
        msg = '''Unable to retrieve JWT with the given credentials:
            User ID: {0}
            Client ID: {1}
            Password: {2}
        '''.format(user_id, client_id, password)
        raise Exception(msg)

def get_uri_context(self):
    headers = self.get_headers()
    if "Authorization" in headers:
        return self.BASE_PROD_URI + '/dna'
    elif 'user-key' in headers:
        return self.BASE_PROD_URI + '/alpha'
    else:
        msg = '''Could not determine user credentials:
            Must specify account credentials as user_id, client_id, and password, either through env vars, customer_config.json, or as args to Listener constructor
            (see README.rst)'''
        raise Exception(msg)

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

def user_key(self):
    if self.account_id is not None:
        user_key = self.account_id
    else:
        user_key = os.getenv(self.ENV_VAR_USER_KEY)

        if user_key is None:
            user_key = self._user_key_id_from_file()

    return user_key

def _user_key_id_from_file(self):
    if not self.initialized:
        self._initialize()

    return self.customer_config.get('user_key')


def _get_requests():
    return requests
