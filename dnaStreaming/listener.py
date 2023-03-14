import time
import requests
import json
from threading import Thread

from google.api_core.exceptions import GoogleAPICallError, NotFound
from google import pubsub_v1

from dnaStreaming import logger
from dnaStreaming.config import Config
from dnaStreaming.services import pubsub_service, credentials_service


class Listener(object):
    DEFAULT_UNLIMITED_MESSAGES = None

    def __init__(self, service_account_id=None, user_key=None, config_file=None):
        config = Config(service_account_id, user_key, config_file)
        self._initialize(config)
        self.current_subscription_index = 0

    def _initialize(self, config):
        self.config = config

    def listen(self, on_message_callback, maximum_messages=DEFAULT_UNLIMITED_MESSAGES, subscription_id="", batch_size=10):
        pubsub_client = pubsub_service.get_client(self.config)

        subscription_id = subscription_id or self.config.subscription()
        if not subscription_id:
            raise Exception(
                'No subscription specified. You must specify the subscription ID either through an environment ' +
                'variable, a config file or by passing the value to the method.')

        streaming_credentials = credentials_service.fetch_credentials(
            self.config)
        subscription_path = pubsub_client.subscription_path(
            streaming_credentials['project_id'], subscription_id)

        logger.info(
            'Listeners for subscriptions have been configured, set and await message arrival.')

        count = 0
        while maximum_messages is None or count < maximum_messages:
            try:
                if maximum_messages is not None:
                    batch_size = min(batch_size, maximum_messages - count)

                pull_request = pubsub_v1.PullRequest(
                    subscription=subscription_path,
                    max_messages=batch_size,
                )
                results = pubsub_client.pull(request=pull_request)

                if results:
                    if len(results.received_messages) > 0:
                        for message in results.received_messages:

                            pubsub_msg = json.loads(message.message.data)
                            logger.info("Received news message with ID: {}".format(
                                pubsub_msg['data'][0]['id']))
                            news_msg = pubsub_msg['data'][0]['attributes']

                            keep_message_flow = on_message_callback(
                                news_msg, subscription_id)

                            if not keep_message_flow:
                                logger.info(
                                    'Callback function returned False or falsy. Message flow stopped.')
                                return

                            ack_request = {
                                "subscription": subscription_path,
                                "ack_ids": [message.ack_id],
                            }
                            pubsub_client.acknowledge(request=ack_request)
                            count += 1

            except GoogleAPICallError as e:
                if isinstance(e, NotFound):
                    raise e
                logger.error(
                    "Encountered a problem while trying to pull a message from a stream. Error is as follows: {}".format(str(e)))
                logger.error("Due to the previous error, system will pause 10 seconds. System will then attempt to pull the message from "
                             "the stream again.")
                time.sleep(10)
                pubsub_client = pubsub_service.get_client(self.config)

    def listen_async(self, on_message_callback, subscription_id=""):
        def ack_message_and_callback(message):
            pubsub_msg = json.loads(message.data)
            logger.info("Received news message with ID: {}".format(
                pubsub_msg['data'][0]['id']))
            news_msg = pubsub_msg['data'][0]['attributes']
            on_message_callback(news_msg, subscription_id)
            message.ack()

        pubsub_client = pubsub_service.get_client(self.config)

        subscription_id = subscription_id or self.config.subscription()

        if not subscription_id:
            raise Exception(
                'No subscription specified. You must specify the subscription ID either through an environment variable, a config file or '
                'by passing the value to the method.')

        streaming_credentials = credentials_service.fetch_credentials(
            self.config)
        subscription_path = pubsub_client.subscription_path(
            streaming_credentials['project_id'], subscription_id)
        subscription = pubsub_client.subscribe(
            subscription_path, callback=ack_message_and_callback)
        logger.info(
            'Listeners for subscriptions have been configured, set and await message arrival.')
        return subscription
