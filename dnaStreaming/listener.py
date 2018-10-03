from __future__ import absolute_import, division, print_function

import time

from dnaStreaming import logger
from dnaStreaming.config import Config
from dnaStreaming.services import pubsub_service, credentials_service


class Listener(object):
    DEFAULT_UNLIMITED_MESSAGES = None

    def __init__(self, service_account_id=None, user_id=None, client_id=None, password=None):
        config = Config(service_account_id, user_id, client_id, password)
        self._initialize(config)
        self.current_subscription_index = 0

    def _initialize(self, config):
        self.config = config

    def listen(self, on_message_callback, maximum_messages=DEFAULT_UNLIMITED_MESSAGES, subscription_id="", batch_size=10):
        pubsub_client = pubsub_service.get_client(self.config)

        subscription_id = subscription_id or self.config.subscription()
        if not subscription_id.strip():
            raise Exception(
                'No subscription specified. You must specify the subscription ID either through an environment variable, a config file or by passing the value to the method.')

        streaming_credentials = credentials_service.fetch_credentials(self.config)
        subscription_path = pubsub_client.subscription_path(streaming_credentials['project_id'], subscription_id)
        logger.info('Listeners for subscriptions have been configured, set and await message arrival.')

        count = 0
        while maximum_messages is None or count <= maximum_messages:
            try:
                if maximum_messages is not None:
                    batch_size = min(batch_size, maximum_messages - count)
                results = pubsub_client.pull(subscription_path, max_messages=batch_size, return_immediately=True)
                if results:
                    for message in results.received_messages:
                        callback_result = on_message_callback(message.message, subscription_id)
                        pubsub_client.acknowledge(subscription_path, [message.ack_id])
                        if not callback_result:
                            break
                        count += 1
                        if maximum_messages is not None and count >= maximum_messages:
                            return

            except Exception as e:
                logger.error("Encountered a problem while trying to pull a message from a stream. Error is as follows: {}".format(str(e)))
                logger.error("Due to the previous error, system will pause 10 seconds. System will then attempt to pull the message from the stream again.")
                time.sleep(10)
                pubsub_client = pubsub_service.get_client(self.config)

    def listen_async(self, on_message_callback, subscription_id=""):
        def ack_message_and_callback(message):
            on_message_callback(message, subscription_id)
            message.ack()

        pubsub_client = pubsub_service.get_client(self.config)

        subscription_id = subscription_id or self.config.subscription()

        if not subscription_id.strip():
            raise Exception(
                'No subscription specified. You must specify the subscription ID either through an environment variable, a config file or by passing the value to the method.')

        streaming_credentials = credentials_service.fetch_credentials(self.config)
        subscription_path = pubsub_client.subscription_path(streaming_credentials['project_id'], subscription_id)
        subscription = pubsub_client.subscribe(subscription_path, callback=ack_message_and_callback)
        logger.info('Listeners for subscriptions have been configured, set and await message arrival.')
        return subscription
