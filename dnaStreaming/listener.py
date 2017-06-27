import google

from dnaStreaming.config import Config
from dnaStreaming.services import pubsub_service


class Listener(object):
    DEFAULT_UNLIMITED_MESSAGES = -1

    def __init__(self, service_account_id=None):
        config = Config(service_account_id)
        self._initialize(config)
        self.current_subscription_index = 0

    def _initialize(self, config):
        self.config = config

    def listen(self, on_message_callback, maximum_messages=DEFAULT_UNLIMITED_MESSAGES, subscription_id=None):
        limit_pull_calls = not (maximum_messages == self.DEFAULT_UNLIMITED_MESSAGES)
        pubsub_client = pubsub_service.get_client(self.config)

        subscription_id = subscription_id if subscription_id is not None else self.config.subscription()

        if subscription_id is None or subscription_id.strip() == '':
            raise Exception(
                'No subscription specified. You must specify the subscription ID either through an environment variable, a config file or by passing the value to the method.')

        subscription = google.cloud.pubsub.subscription.Subscription(subscription_id, client=pubsub_client)

        print('Listeners for subscriptions have been configured, set and await message arrival.')

        count = 0
        while True:
            results = subscription.pull(return_immediately=True)

            if results:
                count += 1
                subscription.acknowledge([ack_id for ack_id, message in results])

                print "Count: {}".format(count)

                callback_result = on_message_callback(message, subscription_id)

                if not callback_result:
                    break

                if limit_pull_calls:
                    maximum_messages -= 1
                    if maximum_messages <= 0:
                        return
