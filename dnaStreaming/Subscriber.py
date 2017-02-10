from google.cloud import pubsub
from dnaStreaming import Config


# ''' Class that allows you to subscribe to a Dow Jones topic feed. This is a singleton. '''
class Subscriber():
    def __init__(self):
        self.stop_subscription = False

        config = Config.Config()
        self.g_cloud_project_name = config.get_google_cloud_project_name()

        self.user_key = config.get_user_key()
        self.topic = config.get_topic()

    def subscription(self, pubsub_client, topic_name):
        topic = pubsub_client.topic(topic_name)
        name = topic_name + '_' + self.user_key
        return topic.subscription(name)

    def halt_subscription_messages(self):
        self.stop_subscription = True

    def get_client(self):
        return pubsub.Client(project=self.g_cloud_project_name, credentials=Config.credentials)

    DEFAULT_UNLIMITED_MESSAGES = -1

    def subscribe(self, on_message_callback, topic_name=None, maximum_messages=DEFAULT_UNLIMITED_MESSAGES):
        if topic_name is None:
            topic_name = self.topic

        limit_pull_calls = not (maximum_messages == self.DEFAULT_UNLIMITED_MESSAGES)
        pubsub_client = self.get_client()

        subscription = self.subscription(pubsub_client, topic_name)

        while not self.stop_subscription:

            if limit_pull_calls:
                if maximum_messages <= 0:
                    break

            results = subscription.pull(return_immediately=False)

            if results:
                subscription.acknowledge([ack_id for ack_id, message in results])
                callback_result = on_message_callback(message, topic_name)

                if not callback_result:
                    break

                if limit_pull_calls:
                    maximum_messages -= 1
