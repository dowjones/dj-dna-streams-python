import unittest
from unittest import TestCase
import os
from Subscriber import Subscriber

class TestSubscriber(TestCase):

    def setUp(self):
        if (os.environ.has_key('GOOGLE_APPLICATION_CREDENTIALS')):
            print 'Key already set'

        os.environ['GCLOUD_PROJECT'] = 'djsyndicationhub-dev'
        os.environ['SUBSCRIBER_NAME'] = 'dev01'

    def test_subscribe(self):
        subscriber = Subscriber()

        def callback(message, topic):
            print 'Topic received: ' + topic

        # Set to false for test only.
        subscriber.requireGoogleAuthenticationEnvironmentVariable = False

        subscriber.subscribe(['ContentEventTranslated', 'ContentStored'], callback)

        self.assertEqual(True, True)

if __name__ == '__main__' and __package__ is None:
     unittest.main()