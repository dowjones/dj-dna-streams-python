import os
import unittest
import json
from unittest import TestCase
from dnaStreaming import Config


class TestConfig(TestCase):
    GOOGLE_APPLICATION_CREDENTIALS = 'GOOGLE_APPLICATION_CREDENTIALS'

    def setUp(self):
        if (os.environ.has_key(self.GOOGLE_APPLICATION_CREDENTIALS)):
            print('Key already set')

    def test_init_when_no_environment_var(self):

        if (os.environ.has_key(self.GOOGLE_APPLICATION_CREDENTIALS)):
            os.environ.pop(self.GOOGLE_APPLICATION_CREDENTIALS)

        self.assertEqual(True, True)
        self.assertFalse(os.environ.has_key(self.GOOGLE_APPLICATION_CREDENTIALS))

        with self.assertRaises(Exception) as context:
            config = Config()

        print context.exception.message

        self.assertTrue('Did you set it the environment variable \'GOOGLE_APPLICATION_CREDENTIALS\' to the path of your Dow Jones provided security file?' in context.exception.message)

    def test_init_when_credential_file_not_exist(self):

        os.environ[self.GOOGLE_APPLICATION_CREDENTIALS] = './someFileNotExist.txt'

        with self.assertRaises(Exception) as context:
            config = Config()

        self.assertTrue('Does it exist?' in context.exception.message)

    def test_init_with_good_credentials_file(self):

        os.environ[self.GOOGLE_APPLICATION_CREDENTIALS] = './sampleGoogleApplicationCredentials.json'

        config = Config()

        userKey = config.get_user_key()

        self.assertEqual(config.get_user_key(), 'cool-guy')
        self.assertEqual(config.get_google_cloud_project_name(), 'project-awesome')
        self.assertEqual(config.get_topic(), 'ContentEventTranslated')

if __name__ == '__main__' and __package__ is None:
     unittest.main()