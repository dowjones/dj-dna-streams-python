import os
from dnaStreaming.listener import Listener

listener = Listener()
quiet_demo = os.getenv('QUIET_DEMO', "false") == "true"
print("\n[ACTIVITY] Receiving messages (SYNC)...\n[0]", end='')


def callback(message, subscription_id, file_handle=None):
    callback.counter += 1
    if not quiet_demo:
        if message['action'] != 'del':
            print('[INFO] [MSG] [{}]: AN: {}, TITLE: {}'.format(callback.counter, message['an'], message['title']))
        else:
            print('[INFO] [MSG] [{}]: AN: {}, *** DELETE ***'.format(callback.counter, message['an']))
    else:
        if callback.counter % 10 == 0:
            print('[{}]'.format(callback.counter), end='')
        else:
            print('.', end='')
    return True


callback.counter = 0
listener.listen(callback)
