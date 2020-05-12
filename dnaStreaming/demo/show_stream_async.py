import os
from time import sleep
from dnaStreaming.listener import Listener

listener = Listener()
quiet_demo = os.getenv('QUIET_DEMO', "false") == "true"
max_secs = 5
print("\n[ACTIVITY] Receiving messages (ASYNC) for {} seconds...\n[0]".format(max_secs), end='')


def callback(message, subscription_id):
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
future = listener.listen_async(callback)

# Stop receiving messages after 5 seconds
for count in range(0, max_secs):
    sleep(1)

if future.running():
    future.cancel()

print("stop receiving messages")
