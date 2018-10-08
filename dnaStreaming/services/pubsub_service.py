from __future__ import absolute_import, division, print_function

from google.cloud.pubsub_v1 import SubscriberClient

from dnaStreaming.services import authentication_service
from dnaStreaming.services import credentials_service


def get_client(config):
    streaming_credentials = credentials_service.fetch_credentials(config)
    credentials = authentication_service.get_authenticated_oauth_credentials(streaming_credentials)

    return SubscriberClient(credentials=credentials)
