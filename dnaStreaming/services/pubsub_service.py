from __future__ import absolute_import, division, print_function

from google.cloud.pubsub_v1 import SubscriberClient

from dnaStreaming.services import authentication_service
from dnaStreaming.services import credentials_service
from dnaStreaming.services.availability_service import MAIN_REGION, BACKUP_REGION


def get_client(config, region=None):
    streaming_credentials = credentials_service.fetch_credentials(config)
    credentials = authentication_service.get_authenticated_oauth_credentials(streaming_credentials)

    if region in (MAIN_REGION, BACKUP_REGION):
        client_options = {"api_endpoint": f"{region}-pubsub.googleapis.com:443"}
    else:
        client_options = {"api_endpoint": "pubsub.googleapis.com:443"}

    return SubscriberClient(credentials=credentials, client_options=client_options)
