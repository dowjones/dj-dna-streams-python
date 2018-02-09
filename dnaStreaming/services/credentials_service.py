import json

import requests


def fetch_credentials(config):
    response = _get_requests().get(config.credentials_uri(), headers=_get_headers(config))

    streaming_credentials_string = json.loads(response.text)['data']['attributes']['streaming_credentials']

    return json.loads(streaming_credentials_string)


def _get_headers(config):
    if config.oauth2_credentials():
        return {
            'Authorization': _fetch_jwt(config)
        }
    else:
        return {
            'user-key': config.service_account_id()
        }


def _fetch_jwt(config):
    oauth2_credentials = config.oauth2_credentials()

    # two requests need to be made, to the same URL, with slightly different params, to finally obtain a JWT
    # the second request contains params returned in the response of the first request
    # I know this makes no sense but it is what it is
    body = {
        'username': oauth2_credentials['user_id'],
        'client_id': oauth2_credentials['client_id'],
        'password': oauth2_credentials['password'],
        'connection': 'service-account',
        'grant_type': 'password',
        'scope': 'openid service_account_id'
    }

    response = _get_requests().post(config.OAUTH_URL, data=body).json()
    
    body['scope'] = 'openid pib'
    body['grant_type'] = 'urn:ietf:params:oauth:grant-type:jwt-bearer'
    body['access_token'] = response['access_token']
    body['assertion'] = response['id_token']

    response = _get_requests().post(config.OAUTH_URL, data=body).json()

    return '{0} {1}'.format(response['token_type'], response['access_token'])


def _get_requests():
    return requests
