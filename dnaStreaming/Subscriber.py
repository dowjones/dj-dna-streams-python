import os
from google.cloud import pubsub
from dnaStreaming import Config

# ''' Class that allows you to subscribe to a Dow Jones topic feed. This is a singleton. '''
class Subscriber():

    def __init__(self):
        self.stop_subscription = False

        config = Config.Config()
        self.gCloudProjectName = config.get_google_cloud_project_name()

        self.userKey = config.get_user_key()
        self.topic = config.get_topic()

    def subscription(self, pubsub_client, topic_name):
        topic = pubsub_client.topic(topic_name)
        name = topic_name + "_Live_" + self.user_key()
        return topic.subscription(name)

    def halt_subscription_messages(self):
        self.stop_subscription = True

    def get_client(self):
        return pubsub.Client(project=self.gCloudProjectName)

    DEFAULT_UNLIMITED_MESSAGES = -1
    def subscribe(self, on_message_callback, topic_name=None, maximum_messages=DEFAULT_UNLIMITED_MESSAGES):
        if topic_name is None:
            topic_name = self.topic

        limitPullCalls = not (maximum_messages == self.DEFAULT_UNLIMITED_MESSAGES)
        pubsub_client = self.get_client()

        subscription = self.subscription(pubsub_client, topic_name)

        while self.stop_subscription != True:

            if limitPullCalls:
                if (maximum_messages <= 0):
                    break

            results = subscription.pull(return_immediately=False)

            if results:
                subscription.acknowledge([ack_id for ack_id, message in results])
                on_message_callback(message, topic_name)

                if limitPullCalls:
                    maximum_messages -= 1

