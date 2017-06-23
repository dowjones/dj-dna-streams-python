import os
import unittest
from unittest import TestCase

from PatchMixin import PatchMixin
from dnaStreaming.config import Config


class TestConfig(TestCase, PatchMixin):
    def setUp(self):
        self.patch_module(os.access, True)

    def tearDown(self):
        self.ensure_remove_environment_variable(Config.ENV_VAR_SERVICE_ACCOUNT_ID)
        self.ensure_remove_environment_variable(Config.ENV_VAR_SUBSCRIPTION_IDS)
        self.ensure_remove_environment_variable(Config.ENV_VAR_CREDENTIALS_URI)

    def ensure_remove_environment_variable(self, key):
        if key in os.environ:
            os.environ.pop(key)

    def test_customer_config_not_found_success(self):
        # Arrange
        config = Config()
        path_bogus = '\\does\\not\\exist'
        config.customer_config_path = path_bogus

        error_message_expected = 'Encountered problem finding \'customer_config.json\' at path \'\\does\\not\\exist\'. Does it exist?'

        # Act
        was_exception_thrown = False

        error_message_actual = None
        try:
            config._validate()
        except Exception as ex:
            error_message_actual = ex.message
            was_exception_thrown = True

        # Assert
        assert was_exception_thrown
        assert error_message_expected == error_message_actual

    def test_get_service_account_and_subs_success(self):
        # Arrange
        config = Config()
        config._set_customer_config_path(os.path.abspath('./test_customer_config.json'))

        # Act
        service_account_id = config.service_account_id()
        subscriptions = config.subscriptions()

        # Assert
        assert service_account_id
        assert isinstance(subscriptions, list)
        assert len(subscriptions) == 2
        assert subscriptions[0] == 'bar'

    def test_environment_variables_success(self):
        # Arrange
        os.environ[Config.ENV_VAR_SERVICE_ACCOUNT_ID] = '123'
        os.environ[Config.ENV_VAR_SUBSCRIPTION_IDS] = 'ABC,DEF'
        os.environ[Config.ENV_VAR_CREDENTIALS_URI] = 'http://hiptotherythum.com'

        # Act
        config = Config()
        config.customer_config_path = os.path.abspath('./test_customer_config.json')
        config._initialize()

        # Assert
        assert os.environ[Config.ENV_VAR_SERVICE_ACCOUNT_ID] == config.service_account_id()
        subscription_ids = config.subscriptions()
        assert len(subscription_ids) == 2
        assert subscription_ids[0] == 'ABC'
        assert subscription_ids[1] == 'DEF'
        assert os.environ[Config.ENV_VAR_CREDENTIALS_URI] == config.credentials_uri()

    def test_account_id_passed_success(self):
        # Arrange
        # Act
        config = Config(account_id='123')

        # Assert
        print config.service_account_id()
        assert config.service_account_id() == '123'


if __name__ == '__main__' and __package__ is None:
    unittest.main()
