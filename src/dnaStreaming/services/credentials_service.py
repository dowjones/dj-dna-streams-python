from __future__ import absolute_import, division, print_function

import json

import requests

SUBSCRIPTION_ID_HEADER = "X-Subscription-Id"


def fetch_credentials(config, subscription_id=None):
    # Copy the cached auth headers so the per-subscription header is not persisted in the config.
    headers = dict(config.get_headers())
    if subscription_id:
        headers[SUBSCRIPTION_ID_HEADER] = subscription_id

    response = requests.get(
        config.get_uri_context() + "/sns-accounts/streaming-credentials",
        headers=headers,
    )

    if response.status_code == 401:
        msg = """Extraction API authentication failed for given credentials header:
            {0}""".format(config.headers)
        raise Exception(msg)

    try:
        streaming_credentials_string = json.loads(response.text)["data"]["attributes"][
            "streaming_credentials"
        ]
    except KeyError:
        raise Exception("Unable to find streaming credentials for given account")

    return json.loads(streaming_credentials_string)
