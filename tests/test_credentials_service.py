import json
from unittest.mock import MagicMock, patch

import pytest

from dnaStreaming.config import Config
from dnaStreaming.services import credentials_service, pubsub_service
from dnaStreaming.services.availability_service import MAIN_REGION
from dnaStreaming.services.credentials_service import SUBSCRIPTION_ID_HEADER

STREAMING_CREDENTIALS = {"project_id": "p"}


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    for var in (
        Config.ENV_VAR_OAUTH_TOKEN,
        Config.ENV_VAR_USER_KEY,
        Config.ENV_VAR_SERVICE_ACCOUNT_ID,
        Config.ENV_VAR_API_HOST,
    ):
        monkeypatch.delenv(var, raising=False)


@pytest.fixture
def config():
    return Config(oauth_token="tok")


@pytest.fixture
def mock_get():
    response = MagicMock()
    response.status_code = 200
    response.text = json.dumps(
        {
            "data": {
                "attributes": {
                    "streaming_credentials": json.dumps(STREAMING_CREDENTIALS)
                }
            }
        }
    )
    with patch.object(
        credentials_service.requests, "get", return_value=response
    ) as mocked:
        yield mocked


def test_fetch_credentials_sends_subscription_id_header(config, mock_get):
    result = credentials_service.fetch_credentials(config, "sub-123")

    url = mock_get.call_args.args[0]
    headers = mock_get.call_args.kwargs["headers"]
    assert url.endswith("/sns-accounts/streaming-credentials")
    assert headers["Authorization"] == "Bearer tok"
    assert headers[SUBSCRIPTION_ID_HEADER] == "sub-123"
    assert result == STREAMING_CREDENTIALS


def test_fetch_credentials_does_not_mutate_cached_headers(config, mock_get):
    credentials_service.fetch_credentials(config, "sub-123")
    assert SUBSCRIPTION_ID_HEADER not in config.get_headers()

    credentials_service.fetch_credentials(config, "sub-456")
    headers = mock_get.call_args.kwargs["headers"]
    assert headers[SUBSCRIPTION_ID_HEADER] == "sub-456"


def test_fetch_credentials_without_subscription_id_omits_header(config, mock_get):
    credentials_service.fetch_credentials(config)

    headers = mock_get.call_args.kwargs["headers"]
    assert SUBSCRIPTION_ID_HEADER not in headers
    assert headers["Authorization"] == "Bearer tok"


def test_get_client_passes_subscription_id(config):
    with (
        patch.object(
            pubsub_service.credentials_service,
            "fetch_credentials",
            return_value=STREAMING_CREDENTIALS,
        ) as mock_fetch,
        patch.object(
            pubsub_service.authentication_service,
            "get_authenticated_oauth_credentials",
        ),
        patch.object(pubsub_service, "SubscriberClient") as mock_client,
    ):
        pubsub_service.get_client(config, "sub-123", region=MAIN_REGION)

    mock_fetch.assert_called_once_with(config, "sub-123")
    assert mock_client.call_args.kwargs["client_options"] == {
        "api_endpoint": f"{MAIN_REGION}-pubsub.googleapis.com:443"
    }
