from __future__ import absolute_import, division, print_function

import os
from time import sleep

from dnaStreaming.listener import Listener

listener = Listener()

quiet_demo = os.getenv('QUIET_DEMO', "false") == "true"


def callback(message, subscription_id):
    message = str(message.data)
    if quiet_demo:
        message = message[:50]
    print('Subscription ID: {}: Message: {}'.format(subscription_id, message))


future = listener.listen_async(callback)

# Stop receiving messages after 5 seconds
for count in range(0, 5):
    sleep(1)

if future.running():
    future.cancel()

print("stop receiving messages")
