from __future__ import absolute_import, division, print_function

import google

from dnaStreaming.config import Config
from dnaStreaming.services import pubsub_service
import time
import sys
import requests
from dnaStreaming import logger
from dnaStreaming.services import credentials_service

class Listener(object):
    DEFAULT_UNLIMITED_MESSAGES = -1

    def __init__(self, service_account_id=None, user_id=None, client_id=None, password=None):
        config = Config(service_account_id, user_id, client_id, password)
        self._initialize(config)
        self.current_subscription_index = 0

    def _initialize(self, config):
        self.config = config

    def _is_exceeded(self, subscription_id):
        stream_url = self.config.streams_uri() + '/' + "-".join(subscription_id.split("-")[:4])
        r = requests.get(stream_url, headers=credentials_service.get_authentication_headers(self.config))
        if r.json()['data']['attributes']['job_status'] == "DOC_COUNT_EXCEEDED":
            return True
        return False

    def listen(self, on_message_callback, maximum_messages=DEFAULT_UNLIMITED_MESSAGES, subscription_id=None):
        limit_pull_calls = not (maximum_messages == self.DEFAULT_UNLIMITED_MESSAGES)
        pubsub_client = pubsub_service.get_client(self.config)
        subscription_id = subscription_id if subscription_id is not None else self.config.subscription()

        if subscription_id is None or subscription_id.strip() == '':
            raise Exception(
                'No subscription specified. You must specify the subscription ID either through an environment variable, a config file or by passing the value to the method.')

        if self._is_exceeded(subscription_id):
            raise Exception(
                "Your article limit has been exceeded. Please contact your customer service representitive for more information.")

        subscription = google.cloud.pubsub.subscription.Subscription(subscription_id, client=pubsub_client)

        logger.info('Listeners for subscriptions have been configured, set and await message arrival.')

        count = 0
        while True:
            try:
                results = subscription.pull(return_immediately=True)

                if results:
                    for (ack_id, msg) in results:
                        callback_result = on_message_callback(msg, subscription_id)
                        if not callback_result:
                            break

                        subscription.acknowledge([ack_id])
                        count += 1

                        if limit_pull_calls:
                            maximum_messages -= 1
                            if maximum_messages <= 0:
                                return

            except google.gax.errors.GaxError as e:
                logger.error("Encountered a problem while trying to pull a message from a stream. Error is as follows: {}".format(str(e)))
                logger.error("Due to the previous error, system will pause 10 seconds. System will then attempt to pull the message from the stream again.")
                time.sleep(10)
                pubsub_client = pubsub_service.get_client(self.config)
                subscription = google.cloud.pubsub.subscription.Subscription(subscription_id, client=pubsub_client)
