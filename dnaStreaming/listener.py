import google

from dnaStreaming.config import Config
from dnaStreaming.services import pubsub_service
from subscription_handler import create_subscription_thread
from thread_utils import wait_while_processing


class Listener(object):
    DEFAULT_UNLIMITED_MESSAGES = -1

    def __init__(self, service_account_id=None):
        config = Config(service_account_id)
        self._initialize(config)

    def _initialize(self, config):
        self.config = config

    def listen(self, on_message_callback, maximum_messages=DEFAULT_UNLIMITED_MESSAGES, subscription_ids=None):
        limit_pull_calls = not (maximum_messages == self.DEFAULT_UNLIMITED_MESSAGES)
        pubsub_client = pubsub_service.get_client(self.config)

        subscription_ids = subscription_ids if subscription_ids is not None else self.config.subscriptions()

        if len(subscription_ids) == 0:
            raise Exception('No subscriptions specified. You must specify subscriptions when calling the \'listen\' function.')

        threads = []
        for subscription_id in subscription_ids:
            subscription = google.cloud.pubsub.subscription.Subscription(subscription_id, client=pubsub_client)

            print("Listening to subscription: {}".format(subscription_id))

            thread = create_subscription_thread(limit_pull_calls, maximum_messages, subscription_id, subscription, on_message_callback)
            threads.append(thread)

        print('Listeners for subscriptions have been configured, set and await message arrival.')

        wait_while_processing(threads)
