import threading


def create_subscription_thread(limit_pull_calls, maximum_messages, subscription_id, subscription, on_message_callback):
    thread = threading.Thread(target=_subscribe, args=(limit_pull_calls, maximum_messages, subscription_id, subscription, on_message_callback))
    thread.daemon = True
    thread.start()

    return thread


def _subscribe(limit_pull_calls, maximum_messages, subscription_id, subscription, on_message_callback):
    count = 0

    while True:

        if limit_pull_calls:
            if maximum_messages <= 0:
                break

        results = subscription.pull(return_immediately=False)

        if results:
            subscription.acknowledge([ack_id for ack_id, message in results])
            count += 1
            print('Count: {}'.format(count))
            callback_result = on_message_callback(message, subscription_id)

            if not callback_result:
                break

            if limit_pull_calls:
                maximum_messages -= 1
