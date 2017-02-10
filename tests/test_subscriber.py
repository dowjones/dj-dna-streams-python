import os
import unittest
import json
from unittest import TestCase


class TestSubscriber(TestCase):
    DAC = 'DOW_JONES_APPLICATION_CREDENTIALS'
    message_count = 0

    def setUp(self):
        os.environ[self.DAC] = './sampleGoogleApplicationCredentials.json'

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

        class StubClient(object):
            pass

        subscriber.get_client = StubClient

        subscriber.subscribe(self.callback, maximum_messages=10)

    def callback(self, message, topic):
        self.message_count += 1
        print('Message number {} received. (Topic is \'{}\')'.format(self.message_count, topic))
        return True

    def test_read_credentials(self):
        self.assertEqual(True, True)
        with open('sampleGoogleApplicationCredentials.json', 'r') as f:
            data = json.load(f)

        self.assertEquals(data['dj_dna_streaming']['user_key'], 'cool-guy')


if __name__ == '__main__' and __package__ is None:
    unittest.main()
