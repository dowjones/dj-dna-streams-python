from google.cloud import pubsub

from app.services import authentication_service
from app.services import credentials_service


def get_client():
    streaming_credentials = credentials_service.fetch_credentials()
    credentials = authentication_service.get_authenticated_oauth_credentials(streaming_credentials)

    return pubsub.Client(project=streaming_credentials['project_id'], credentials=credentials)
