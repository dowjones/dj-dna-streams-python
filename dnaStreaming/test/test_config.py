from __future__ import absolute_import, division, print_function

import os
import unittest
from unittest import TestCase

from .PatchMixin import PatchMixin
from dnaStreaming.config import Config

# Python3 has FileNotFoundError defined. Python2 does not.
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


class TestConfig(TestCase, PatchMixin):
    def setUp(self):
        self.patch_module(os.access, True)

    def tearDown(self):
        self.ensure_remove_environment_variable(Config.ENV_VAR_USER_KEY)
        self.ensure_remove_environment_variable(Config.ENV_VAR_SUBSCRIPTION_ID)
        self.ensure_remove_environment_variable(Config.ENV_VAR_EXTRACTION_API_HOST)
        self.ensure_remove_environment_variable(Config.ENV_VAR_USER_ID)
        self.ensure_remove_environment_variable(Config.ENV_VAR_CLIENT_ID)
        self.ensure_remove_environment_variable(Config.ENV_VAR_PASSWORD)

    def ensure_remove_environment_variable(self, key):
        if key in os.environ:
            os.environ.pop(key)

    def test_customer_config_not_found_success(self):
        # Arrange
        config = Config()
        path_bogus = '\\does\\not\\exist'
        config.customer_config_path = path_bogus

        error_message_expected = 'No such file or directory'

        # Act
        was_exception_thrown = False

        error_message_actual = None
        try:
            config._validate()
        except FileNotFoundError as ex:
            error_message_actual = ex.strerror
            error_message_filename = ex.filename
            was_exception_thrown = True

        # Assert
        assert was_exception_thrown
        assert error_message_expected == error_message_actual
        assert path_bogus == error_message_filename

    def test_get_vals_from_file_success(self):
        # Arrange
        config = Config()

        fileFolder = os.path.dirname(os.path.realpath(__file__))
        config._set_customer_config_path(os.path.join(fileFolder, 'test_customer_config.json'))

        # Act
        user_key = config.get_user_key()
        subscription = config.subscription()
        oauth2_credentials = config.oauth2_credentials()

        # Assert
        assert user_key
        assert subscription == 'bar'
        assert oauth2_credentials.get('user_id')
        assert oauth2_credentials.get('password')
        assert oauth2_credentials.get('client_id')

    def test_environment_variables_success(self):
        # Arrange
        os.environ[Config.ENV_VAR_USER_KEY] = '123'
        os.environ[Config.ENV_VAR_SUBSCRIPTION_ID] = 'ABC'
        os.environ[Config.ENV_VAR_EXTRACTION_API_HOST] = 'http://hiptotherythum.com'
        os.environ[Config.ENV_VAR_USER_ID] = 'user'
        os.environ[Config.ENV_VAR_CLIENT_ID] = 'client'
        os.environ[Config.ENV_VAR_PASSWORD] = 'password'

        # Act
        config = Config()
        fileFolder = os.path.dirname(os.path.realpath(__file__))
        config._set_customer_config_path(os.path.join(fileFolder, 'test_customer_config.json'))
        config._initialize()

        # Assert
        assert os.environ[Config.ENV_VAR_USER_KEY] == config.get_user_key()
        subscription_id = config.subscription()
        assert subscription_id == 'ABC'
        assert os.environ[Config.ENV_VAR_USER_ID] == config.oauth2_credentials().get('user_id')
        assert os.environ[Config.ENV_VAR_CLIENT_ID] == config.oauth2_credentials().get('client_id')
        assert os.environ[Config.ENV_VAR_PASSWORD] == config.oauth2_credentials().get('password')

    def test_oauth2_creds_not_provided(self):
        # Arrange
        config = Config()

        # Act
        creds = config.oauth2_credentials()

        # Assert
        assert creds is None

    def test_user_key_passed_success(self):
        # Arrange
        # Act
        config = Config(user_key='123')

        # Assert
        print(config.get_user_key())
        assert config.get_user_key() == '123'

    def test_get_headers_jwt(self):
        # Arrange
        config = Config()

        fileFolder = os.path.dirname(os.path.realpath(__file__))
        config._set_customer_config_path(os.path.join(fileFolder, 'test_customer_config.json'))

        jwt = "Bearer of Bad News"
        fetch_jwt_mock = self.patch_module(config._fetch_jwt, jwt)

        headers_expected = {
            'Authorization': jwt
        }

        # Act
        headers_actual = config.get_authentication_headers()

        # Assert
        assert headers_actual == headers_expected
        fetch_jwt_mock.assert_called_once()

    def test_get_headers_user_key(self):
        # Arrange
        user_key = "just some user key"
        config = Config(user_key)

        headers_expected = {
            'user-key': user_key
        }

        fetch_jwt_mock = self.patch_module(config._fetch_jwt, '')

        # Act
        headers_actual = config.get_authentication_headers()

        # Assert
        assert headers_actual == headers_expected
        fetch_jwt_mock.assert_not_called()



if __name__ == '__main__' and __package__ is None:
    unittest.main()
