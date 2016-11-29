import os
from google.cloud import pubsub

# ''' Class that allows you to subscribe to a Dow Jones topic feed. This is a singleton. '''
class Subscriber():

    def __init__(self):
        self.gCloudProjectName = os.environ['GCLOUD_PROJECT'] if (os.environ.has_key('GCLOUD_PROJECT')) else 'djsyndicationhub'
        self.require_google_authentication_environment_variable = True
        self.stop_subscription = False

    def user_key(self):
        if os.environ.has_key('USER_KEY') != True:
            raise Exception("You need to set the environment variable \'USER_KEY\' to your Dow Jones provided subscriber name value.")

        return os.environ['USER_KEY']

    def subscription(self, pubsub_client, topic_name):
        topic = pubsub_client.topic(topic_name)
        name = topic_name + "_Live_" + self.user_key()
        return topic.subscription(name)

    def halt_subscription_messages(self):
        self.stop_subscription = True

    DEFAULT_TOPIC_NAME = 'ContentEventTranslated'
    def subscribe(self, on_message_callback, topic_name=DEFAULT_TOPIC_NAME):
        pubsub_client = pubsub.Client()

        if (self.require_google_authentication_environment_variable and os.environ.has_key('GOOGLE_APPLICATION_CREDENTIALS') != True):
            raise Exception('You need to set the environment variable \'GOOGLE_APPLICATION_CREDENTIALS\' to the path of your Dow Jones provided security file.')

        subscription = self.subscription(pubsub_client, topic_name)

        while self.stop_subscription != True:
            results = subscription.pull(return_immediately=False)

            if results:
                subscription.acknowledge([ack_id for ack_id, message in results])
                on_message_callback(message, topic_name)
