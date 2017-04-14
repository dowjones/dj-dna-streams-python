from unittest import TestCase
import os
import logging
from tests import TEST_DIR
from dnaStreaming.listener import Listener


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class TestListener(TestCase):
    message_count = 0

    def setUp(self):
        os.environ['DOW_JONES_APPLICATION_CREDENTIALS'] = os.path.join(TEST_DIR, 'dowJonesApplicationCredentials.json')

    def callback(self, message, subscription_name):
        self.message_count += 1
        log.info('Message: {}; Data {}'.format(self.message_count, message.data.__str__()))
        return True

    def test_listener(self):
        listener = Listener()

        maximum_messages = 10

        listener.listen(self.callback, maximum_messages)

        assert listener is not None
