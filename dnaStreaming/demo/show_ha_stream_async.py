import os
from time import sleep
from dnaStreaming.listener import Listener

listener = Listener()
quiet_demo = os.getenv('QUIET_DEMO', "false") == "true"
max_secs = 1000
print("\n[ACTIVITY] Receiving messages (ASYNC) for {} seconds...\n[0]".format(max_secs), end='')


def callback(message, subscription_id):
    callback.counter += 1
    if not quiet_demo:
        if message['action'] != 'del':
            print('[INFO] [SUBSCRIPTION]: {} [MSG] [{}]: AN: {}, TITLE: {}'.format(subscription_id, callback.counter, message['an'], message['title']))
        else:
            print('[INFO] [SUBSCRIPTION]: {} [MSG] [{}]: AN: {}, *** DELETE ***'.format(subscription_id, callback.counter, message['an']))
    else:
        if callback.counter % 10 == 0:
            print('[{}]'.format(callback.counter), end='')
        else:
            print('.', end='')
    return True


callback.counter = 0
listener_controller = listener.listen_async_ha(callback)

# Stop receiving messages after 5 seconds
for count in range(0, max_secs):
    sleep(1)

if listener_controller.listener_is_running():
    listener_controller.stop_listener()

print("stop receiving messages")
