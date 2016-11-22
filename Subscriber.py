import os
from google.cloud import pubsub

# ''' Class that allows you to subscribe to a Dow Jones topic feed. This is a singleton. '''

class Subscriber():
    def __init__(self):
        gCloudProjectName = os.environ['GCLOUD_PROJECT'] if (os.environ.has_key('GCLOUD_PROJECT')) else 'djsyndicationhub'
        self.pubsub_client = pubsub.Client(project=gCloudProjectName)
        self.requireGoogleAuthenticationEnvironmentVariable = True

    def getSubscriberName(self):
        result = os.environ.has_key('SUBSCRIBER_NAME')

        if result != True:
            raise Exception("You need to set the environment variable \'SUBSCRIBER_NAME\' to your Dow Jones provided subscriber name value.")

        return os.environ['SUBSCRIBER_NAME']

    def subscribe(self, topics, onMessageCallback):

        if (self.requireGoogleAuthenticationEnvironmentVariable and os.environ.has_key('GOOGLE_APPLICATION_CREDENTIALS') != True):
            raise Exception('You need to set the environment variable \'GOOGLE_APPLICATION_CREDENTIALS\' to the path of your Dow Jones provided security file.')

        for topicName in topics:
            topic = self.pubsub_client.topic(topicName)

            name = topicName + "_Live_" + self.getSubscriberName()
            subscription = topic.subscription(name)

            # Change return_immediately=False to block until messages are received.
            while True:
                results = subscription.pull(return_immediately=False)

                # Acknowledge received messages. If you do not acknowledge, Pub/Sub will
                # redeliver the message.
                if results:
                    subscription.acknowledge([ack_id for ack_id, message in results])

                onMessageCallback(message, topicName)




