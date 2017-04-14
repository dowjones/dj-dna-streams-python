import google
from google.cloud import pubsub

import Config


class Listener(object):
    DEFAULT_UNLIMITED_MESSAGES = -1

    def __init__(self):
        self.stop_subscription = False

        config = Config.Config()
        self.config = config
        self.g_cloud_project_name = config.get_google_cloud_project_name()

        self.user_key = config.get_user_key()
        self.subscriptions = config.get_subscriptions()

    def get_client(self):
        return pubsub.Client.from_service_account_json(self.config.credentials_path, self.g_cloud_project_name)

    def listen(self, on_message_callback, maximum_messages=DEFAULT_UNLIMITED_MESSAGES):
        limit_pull_calls = not (maximum_messages == self.DEFAULT_UNLIMITED_MESSAGES)
        pubsub_client = self.get_client()

        for subscription in self.subscriptions:
            subscription_name = subscription['name']
            subscription = google.cloud.pubsub.subscription.Subscription(subscription_name, client=pubsub_client)

            while not self.stop_subscription:

                if limit_pull_calls:
                    if maximum_messages <= 0:
                        break

                results = subscription.pull(return_immediately=False)

                if results:
                    subscription.acknowledge([ack_id for ack_id, message in results])
                    callback_result = on_message_callback(message, subscription_name)

                    if not callback_result:
                        break

                    if limit_pull_calls:
                        maximum_messages -= 1
