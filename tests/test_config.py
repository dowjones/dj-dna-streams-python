import os
import unittest
from unittest import TestCase

from dnaStreaming.Config import Config
from tests import TEST_DIR


class TestConfig(TestCase):
    DOW_JONES_APPLICATION_CREDENTIALS = 'DOW_JONES_APPLICATION_CREDENTIALS'

    def setUp(self):
        if self.DOW_JONES_APPLICATION_CREDENTIALS in os.environ:
            print('Key already set')

    def test_init_when_no_environment_var(self):

        if self.DOW_JONES_APPLICATION_CREDENTIALS in os.environ:
            os.environ.pop(self.DOW_JONES_APPLICATION_CREDENTIALS)

        self.assertEqual(True, True)
        self.assertFalse(self.DOW_JONES_APPLICATION_CREDENTIALS in os.environ)

        with self.assertRaises(Exception) as context:
            Config()

        self.assertTrue('Encountered problem reading required environmental variable ' +
                        '\'DOW_JONES_APPLICATION_CREDENTIALS\'.Did you set the environment variable ' +
                        '\'DOW_JONES_APPLICATION_CREDENTIALS\' to the path of your Dow Jones provided ' +
                        'security file?' in context.exception.message)

    def test_init_when_credential_file_not_exist(self):

        os.environ[self.DOW_JONES_APPLICATION_CREDENTIALS] = './someFileNotExist.txt'

        with self.assertRaises(Exception) as context:
            Config()

        self.assertTrue('Does it exist?' in context.exception.message)

    def test_init_with_good_credentials_file(self):

        os.environ[self.DOW_JONES_APPLICATION_CREDENTIALS] = os.path.join(TEST_DIR, 'sampleCredentials.json')

        config = Config()

        self.assertEqual(config.get_user_key(), 'cust-key-sample-123A')
        self.assertEqual(config.get_google_cloud_project_name(), 'project-awesome')

    def test_get_google_project_name_when_blank_passed(self):

        os.environ[self.DOW_JONES_APPLICATION_CREDENTIALS] = os.path.join(TEST_DIR, 'sampleCredentials.json')

        config = Config()

        config.credentials[config.DOW_JONES_CONFIG_KEY]['project_name'] = ''

        assert config.get_google_cloud_project_name() == 'djsyndicationhub-prod'

    def test_get_google_project_name_when_none_passed(self):

        os.environ[self.DOW_JONES_APPLICATION_CREDENTIALS] = os.path.join(TEST_DIR, 'sampleCredentials.json')

        config = Config()

        config.credentials[config.DOW_JONES_CONFIG_KEY]['project_name'] = None

        assert config.get_google_cloud_project_name() == 'djsyndicationhub-prod'

    def test_get_google_project_name_when_no_key_passed(self):

        os.environ[self.DOW_JONES_APPLICATION_CREDENTIALS] = os.path.join(TEST_DIR, 'sampleCredentials.json')

        config = Config()

        config.credentials[config.DOW_JONES_CONFIG_KEY].pop('project_name', None)

        assert config.get_google_cloud_project_name() == 'djsyndicationhub-prod'


if __name__ == '__main__' and __package__ is None:
    unittest.main()
