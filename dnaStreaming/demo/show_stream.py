from dnaStreaming.listener import Listener

listener = Listener()


def callback(message, subscription_id):
    print('Subscription ID: {}: Message: {}'.format(subscription_id, message.data.__str__()))
    return True  # If desired return False to stop the message flow. This will unblock the process as well.


listener.listen(callback, maximum_messages=10)  # Omitting maximum_messages means you will continue to get messages as they appear. Can be a firehose. Use with caution.
