import os
from dnaStreaming.listener import Listener

listener = Listener()

quiet_demo = os.getenv('QUIET_DEMO', 'false')

print ('Is quiet demo true? ' + str(quiet_demo == True))

def callback(message, subscription_id):
    message = message.data.__str__()
    if quiet_demo == 'true':
        message = message[:50]
    print('Subscription ID: {}: Message: {}'.format(subscription_id, message))
    return True  # If desired return False to stop the message flow. This will unblock the process as well.


listener.listen(callback, maximum_messages=10)  # Omitting maximum_messages means you will continue to get messages as they appear. Can be a firehose. Use with caution.
