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

    def listen(self, on_message_callback, maximum_messages=DEFAULT_UNLIMITED_MESSAGES, subscription_ids=None):
        limit_pull_calls = not (maximum_messages == self.DEFAULT_UNLIMITED_MESSAGES)
        pubsub_client = pubsub_service.get_client(self.config)

        subscription_ids = subscription_ids if subscription_ids is not None else self.config.subscriptions()

        if len(subscription_ids) == 0:
            raise Exception('No subscriptions specified. You must specify subscriptions when calling the \'listen\' function.')

        subscription_pullers = []
        for subscription_id in subscription_ids:
            subscription = google.cloud.pubsub.subscription.Subscription(subscription_id, client=pubsub_client)
            subscription_pullers.append(subscription)

        print('Listeners for subscriptions have been configured, set and await message arrival.')

        current_sub_puller = -1
        count = 0
        while True:
            subscription, current_sub_puller = self.get_next_subscription_id(current_sub_puller, subscription_pullers)

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

    def get_next_subscription_id(self, current_subscription_index, subscriptions):
        if len(subscriptions) <= current_subscription_index + 1:
            current_subscription_index = 0
        else:
            current_subscription_index += 1

        sub = subscriptions[current_subscription_index]

        return sub, current_subscription_index
