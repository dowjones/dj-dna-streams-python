import os
import unittest
from unittest import TestCase


class TestSubscriber(TestCase):

    def setUp(self):
        if (os.environ.has_key('GOOGLE_APPLICATION_CREDENTIALS')):
            print('Key already set')

        os.environ['GCLOUD_PROJECT'] = 'djsyndicationhub-dev'
        os.environ['USER_KEY'] = 'dev01'

    def test_subscribe(self):

        from sub.Subscriber import Subscriber
        subscriber = Subscriber()

        class StubSubscription():

            def __init__(self, pubsub_client, topic_name):
                pass

            def pull(self, return_immediately):
                return [('ack_id234', object())]

            def acknowledge(self, foo):
                pass


        subscriber.subscription = StubSubscription

        def callback(message, topic):
            print('Topic received: ' + topic)

        # Set to false for test only.
        subscriber.require_google_authentication_environment_variable = False

        subscriber.subscribe(callback)

if __name__ == '__main__' and __package__ is None:
     unittest.main()