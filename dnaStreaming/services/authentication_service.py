import httplib2
from oauth2client.service_account import ServiceAccountCredentials

http = httplib2.Http()


def get_authenticated_oauth_credentials(streaming_credentials):
    service_account_cred = ServiceAccountCredentials.from_json_keyfile_dict(streaming_credentials)
    service_account_cred.authorize(http)

    return service_account_cred
