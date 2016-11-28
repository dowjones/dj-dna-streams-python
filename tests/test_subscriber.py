import unittest
from unittest import TestCase
import os
from google.cloud import pubsub
from mock import MagicMock, create_autospec

class TestSubscriber(TestCase):

    def setUp(self):
        if (os.environ.has_key('GOOGLE_APPLICATION_CREDENTIALS')):
            print('Key already set')

        os.environ['GCLOUD_PROJECT'] = 'djsyndicationhub-dev'
        os.environ['USER_KEY'] = 'dev01'

    def test_subscribe(self):

        from Subscriber import Subscriber
        subscriber = Subscriber()

        mock_type_subscription = create_autospec(pubsub.Subscription)
        subscriber.subscription = mock_type_subscription

        def callback(message2, topic):
            print('Topic received: ' + topic)

        # Set to false for test only.
        subscriber.require_google_authentication_environment_variable = False

        subscriber.subscribe(callback)

if __name__ == '__main__' and __package__ is None:
     unittest.main()