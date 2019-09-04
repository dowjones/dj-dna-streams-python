from __future__ import absolute_import, division, print_function

import os
import json
from dnaStreaming.listener import Listener

listener = Listener()

quiet_demo = os.getenv('QUIET_DEMO', "false") == "true"


def callback(message, subscription_id, file_handle = None):
    if type(message) == str:
        decoded = json.loads(message)
        file_handle.write(json.dumps(decoded, ensure_ascii=False) + "\n")
        #print('Subscription ID: {}: Message: {}'.format(subscription_id, message))
        print(".")
    print("$")
    return True

listener.listen(callback)
