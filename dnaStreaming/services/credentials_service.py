import json

import requests


def fetch_credentials(config):
    headers = _get_headers(config)
    response = _get_requests().get(config.credentials_uri(headers), headers=headers)

    if response.status_code == 401:
        msg = '''Extraction API authentication failed for given credentials header:
            {0}'''.format(headers)
        raise Exception(msg)

    try:
        streaming_credentials_string = json.loads(response.text)['data']['attributes']['streaming_credentials']
    except KeyError:
        raise Exception("Unable to find streaming credentials for given account")

    return json.loads(streaming_credentials_string)


def _get_headers(config):
    if config.oauth2_credentials():
        return {
            'Authorization': _fetch_jwt(config)
        }

    # missing oauth creds, authenticate the old way via account ID
    account_id = config.service_account_id()
    if account_id:
        return {
            'user-key': account_id
        }

    # missing oauth creds and account ID, raise exception
    msg = '''Missing credentials:
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


def _get_requests():
    return requests
