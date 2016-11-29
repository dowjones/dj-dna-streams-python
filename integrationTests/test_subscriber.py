import os
import unittest
from unittest import TestCase

from sub import Subscriber

class TestSubscriber(TestCase):

    def setUp(self):
        if (os.environ.has_key('GOOGLE_APPLICATION_CREDENTIALS')):
            print('Key already set')

        os.environ['GCLOUD_PROJECT'] = 'djsyndicationhub-dev'
        os.environ['USER_KEY'] = 'dev01'

    def test_subscribe(self):
        subscriber = Subscriber()

        def callback(message, topic):
            print('Topic: {}: Message: {}'.format(topic, message.data.__str__()))

        # Set to false for test only.
        subscriber.require_google_authentication_environment_variable = False

        subscriber.subscribe(callback, 'ContentEventTranslated')

        self.assertEqual(True, True)

if __name__ == '__main__' and __package__ is None:
     unittest.main()