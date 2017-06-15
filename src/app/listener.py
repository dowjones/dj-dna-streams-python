import google

from app.config import Config
from app.services import pubsub_service


class Listener(object):
    DEFAULT_UNLIMITED_MESSAGES = -1

    def __init__(self, account_id=None):
        self.stop_subscription = False

        config = Config(account_id)
        self._initialize(config)

    def _initialize(self, config):
        self.config = config

    def listen(self, on_message_callback, maximum_messages=DEFAULT_UNLIMITED_MESSAGES):
        limit_pull_calls = not (maximum_messages == self.DEFAULT_UNLIMITED_MESSAGES)
        pubsub_client = pubsub_service.get_client(self.config)

        for subscription_id in self.config.subscriptions():
            subscription = google.cloud.pubsub.subscription.Subscription(subscription_id, client=pubsub_client)

            while not self.stop_subscription:

                if limit_pull_calls:
                    if maximum_messages <= 0:
                        break

                results = subscription.pull(return_immediately=False)

                if results:
                    subscription.acknowledge([ack_id for ack_id, message in results])
                    callback_result = on_message_callback(message, subscription_id)

                    if not callback_result:
                        break

                    if limit_pull_calls:
                        maximum_messages -= 1
