from google.cloud import pubsub

from dnaStreaming.services import credentials_service
from dnaStreaming.services import authentication_service


def get_client(config):
    streaming_credentials = credentials_service.fetch_credentials(config)
    credentials = authentication_service.get_authenticated_oauth_credentials(streaming_credentials)

    return pubsub.Client(project=streaming_credentials['project_id'], credentials=credentials)
