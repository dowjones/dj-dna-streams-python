import json

import requests

from app.config import Config


def fetch_credentials(config):
    headers = {
        'user-key': config.service_account_id()
    }

    response = _get_requests().get(config.credentials_uri(), headers=headers)

    streaming_credentials_string = json.loads(response.text)['data']['attributes']['streaming_credentials']

    return json.loads(streaming_credentials_string)


def _get_requests():
    return requests
