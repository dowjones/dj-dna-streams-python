import os
from dnaStreaming.listener import Listener

listener = Listener()

quiet_demo = os.getenv('QUIET_DEMO', 'false')


def callback(message, subscription_id):
    message = message.data.__str__()
    if quiet_demo == 'true' and len(message) > 50:
        message = message[:50]
    print('Subscription ID: {}: Message: {}'.format(subscription_id, message))
    return True  # If desired return False to stop the message flow. This will unblock the process as well.


listener.listen(callback) 
