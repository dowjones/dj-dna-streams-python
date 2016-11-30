import os
import unittest
import json
from unittest import TestCase

class TestSubscriber(TestCase):
    GAP = 'GOOGLE_APPLICATION_CREDENTIALS'

    def setUp(self):
        if (os.environ.has_key(self.GAP)):
            print('Key already set')

        os.environ[self.GAP] = './sampleGoogleApplicationCredentials.json'

        os.environ['GCLOUD_PROJECT'] = 'djsyndicationhub-dev'
        os.environ['USER_KEY'] = 'dev01'

    def test_subscribe(self):

        from dnaStreaming.Subscriber import Subscriber
        subscriber = Subscriber()

        class StubSubscription():

            def __init__(self, pubsub_client, topic_name):
                pass

            def pull(self, return_immediately):
                return [('ack_id234', object())]

            def acknowledge(self, foo):
                pass


        subscriber.subscription = StubSubscription

        class StubClient():
            pass

        subscriber.get_client = StubClient

        def callback(message, topic):
            print('Topic received: ' + topic)

        subscriber.subscribe(callback, maximum_messages=1)

    def test_read_credentials(self):

        self.assertEqual(True, True)
        with open('sampleGoogleApplicationCredentials.json', 'r') as f:
            data = json.load(f)

        self.assertEquals(data['dj_dna_streaming']['user_key'], 'cool-guy')

if __name__ == '__main__' and __package__ is None:
     unittest.main()