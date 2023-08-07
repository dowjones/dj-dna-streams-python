from __future__ import absolute_import, division, print_function

import json
import requests


def fetch_credentials(config):
    response = _get_requests().get(config.get_uri_context() + '/sns-accounts/streaming-credentials',
                                   headers=config.get_headers())

    if response.status_code == 401:
        msg = '''Extraction API authentication failed for given credentials header:
            {0}'''.format(config.headers)
        raise Exception(msg)

    try:
        streaming_credentials_string = json.loads(response.text)['data']['attributes']['streaming_credentials']
    except KeyError:
        raise Exception("Unable to find streaming credentials for given account")

    return json.loads(streaming_credentials_string)


def _get_requests():
    return requests
