from __future__ import absolute_import, division, print_function

from google.oauth2 import service_account


def get_authenticated_oauth_credentials(streaming_credentials):
    return service_account.Credentials.from_service_account_info(streaming_credentials)
