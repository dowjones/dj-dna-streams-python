import json
from unittest import TestCase

from dnaStreaming.config import Config
from dnaStreaming.services import credentials_service
from dnaStreaming.services import authentication_service
from PatchMixin import PatchMixin


class TestCredentials(TestCase, PatchMixin):
    streaming_credentials = None

    def setUp(self):
        self.streaming_credentials_raw = "{\n \"type\": \"service_account\",\n  \"project_id\": \"djsyndicationhub-dev\",\n  \"private_key_id\": \"63b384dcfa86780ccca38da1baa64fac7aac0e2d\",\n  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCQNzJFTpaXAUGF\\n1p5kGxw3yDHQArxuJuULPTgDcfHCTyWWFVWdXdaBQBsc2sPEqjGBbIvPDOZ00Vf5\\nNFCKrVxXoPYI3RQH40x3Bjt4VEqPIgZ/Xuz2Oas1EAR4pRKYhD0M7luucj8HI2Vz\\nPR0JOdFi94gZhcpwZsXbK2Br+pL9lTyxRmvcBUTP+966afLURARw9SDWcPxFOrta\\nVFoFMd+x7oJdEgyxHefjZlnt0ofBjGBLCu/8KC6WEaZO5xCUoNWV8MlPuDqU0Z/O\\nNPwJXrDUZJw1CiDnIq+qo6MPpn4LVA37S0qRhnMpF7UGdcBqHojhlWDjAoFEoM01\\n2Ccd+pOLAgMBAAECggEALerNIEER9HlrZdQ8MS5qkR42Mf81BLNwmOAAjiRA7/eo\\nRX18eXLvwc5p84l57Iut4IHxj9aRJ9+hrZBpFoZ1ENeIjrDpWEuYRItg8wKPjLwu\\nKm7MbudUqjvz2H/iiFoOYCgiW8w3Yiv0eLkcHhxhHSwoEsxE9P3cAFjyxd6N35wi\\nzvnF/ok4FXltqdO2eErQSzdiI0XGkuxboXqU4KbtFQwXrF0NryFf33S/wERA6UPi\\nkZnaZjkU/7BXzLitSJVaI6p+mOO+HgAYIFFXMdkBLVxuEcsOy8HDdH5Bro4EYBc4\\n1G0yuIhOgaBDAhhhFcCjSvAglEbQEP+Bnrgq/S4q8QKBgQDB3Tcy1OdVHwRKIfEW\\nHuobsikYSmm2GbsIjNOtVlTuuHOgktej+WnWtUNZuPLa+6IN88INvsr7cGOYuBaU\\nN3aLJZ9aKN4HcP+/nd4y1y01IMre2yBooWWhMNm8qbbs9Qm+DKZB03SWTOnuEQNl\\n1AClvnaG0Ry5T1/sXNuajYATOwKBgQC+cEK2weVHbtiWryoHB0bMyo3dXb8mT/lL\\n9Ur1dO14XqM0q43ggsOkUv1dX4NCrmlTrar+o+kId86VQ+w7GtDO1v9WJNefkM9w\\nW09KLBM0To5eHU+xuSv6s7MKrBcx258LnprWVaoucjstyFZALttAIZmnIeWhMSWv\\nDaIULo/b8QKBgFVYwlhKip1azlSkpLKMYZxXzue2uttEcKbO+NGy1ClUYvMqMm0p\\n/IJdwozZc3EcnrdtvNy4RjxzuiUdxjLyR+nyYjkbDMRR5wXAxnWzbV+aVDXQWnA1\\nvbw8+V6piLLBHczhXMBWC1mv+ryoGMrXjoFpXFz16qNaYmx4ZOWhreTJAoGBAI4+\\nHaaSRyZG5iIO7e5YAgr/FF2PIzKDs6qHqhiS4LjyvyadKRjTszvu/O4cZFePHH7z\\nDfCrD2lSy4v0MuOm0OZd8lQuqpu1tyuuGBhHuYRtVKt5a0hNDktwo7/J8H0+FJrC\\nOdb0H2wXyJoWtE22ce+B6VnL2M/AfOw226QFb1CRAoGBAKnehL2TfgQnEW7x49U6\\niEeWNhd/yzTWOi7eaZlmHdBCDkixxHMQEPhIF4aWFBVNDcHEW5SVzqUc6o42T7oj\\n2uCusQOld6ys1OTF1jdmXnEj2rt+zugDCRs3raMLfPBd4TC3Z1/XMjzleP8hpOXZ\\n8CzTRWWijVqYCbmHUw5XmeDp\\n-----END PRIVATE KEY-----\\n\",\n  \"client_email\": \"dowjones@djsyndicationhub-dev.iam.gserviceaccount.com\",\n  \"client_id\": \"102900210428916716582\",\n  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\n  \"token_uri\": \"https://accounts.google.com/o/oauth2/token\",\n  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\n  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/dowjones%40djsyndicationhub-dev.iam.gserviceaccount.com\"\n}"
        self.streaming_credentials = self.streaming_credentials_raw.replace('\\n', '\\\\n').replace('\n', '\\n').replace('"', '\\"')

    def test_fetch_credentials(self):
        # Arrange

        response_expected = '''{
          "data": {
            "attributes": {
              "streaming_credentials": "%s"
            },
            "id": "foo",
            "type": "account_streaming_credentials"
          }
        }'''

        response_expected = response_expected % self.streaming_credentials

        self.patch_module(credentials_service._get_requests, RequestsMock(response_expected))

        config = Config()

        # Act
        credentials = credentials_service.fetch_credentials(config)

        # Assert
        assert credentials
        assert credentials['type'] == 'service_account'

    def test_gc_auth(self):
        streaming_credentials_dict = json.loads(self.streaming_credentials_raw)

        credentials = authentication_service.get_authenticated_oauth_credentials(streaming_credentials_dict)

        from google.cloud import pubsub
        pubsub.Client(project=streaming_credentials_dict['project_id'], credentials=credentials)


class RequestsMock(object):
    def __init__(self, response):
        self.response = response

    def get(self, url, **kwargs):
        return ResponseMock(self.response)


class ResponseMock(object):
    def __init__(self, text):
        self.text = text
