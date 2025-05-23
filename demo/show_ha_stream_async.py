import os
import datetime
from time import sleep
from dnaStreaming.listener import Listener

listener = Listener()
max_secs = 10
print(f"\n[ACTIVITY] Receiving messages (ASYNC) for {max_secs} seconds...")

def print_message(message):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def callback(factiva_message, subscription_id):
    try:
        if 'action' in factiva_message.keys():
            # Message is an article event
            # Implement your logic according to the documentation:
            # https://developer.dowjones.com/documents/site-docs-factiva_apis-factiva_analytics_apis-factiva_streams_api#article-specific-events
            if factiva_message['action'] == 'add':
                # Insert the article to the repository as new. Handle repeated messages.
                print_message(f"[ARTICLE] [ADD] AN: {factiva_message['an']} - {factiva_message['title']}")
            elif factiva_message['action'] == 'rep':
                # Upsert/Update/AddNewVersion the article in the repository. Handle repeated messages.
                print_message(f"[ARTICLE] [REP] AN: {factiva_message['an']} - {factiva_message['title']}")
            elif factiva_message['action'] == 'del':
                # Delete or mark as deleted the article in the repository. Handle inexistent article AN.
                print_message(f"[ARTICLE] [DEL] AN: {factiva_message['an']} - *** DELETE ***")
            else:
                print_message(f"[ERROR] Factiva Action Not Handled: {factiva_message['action']}")
            
        elif 'event_type' in factiva_message.keys():
            # Message is a bulk action or service event
            if factiva_message['event_type'] == 'source_delete':
                # Delete all articles from the repository matching the source_code. Handle inexistent source_code and repeated messages.
                print_message(f"[EVENT] [SOURCE_DELETE] Source: {factiva_message['source_code'].upper()} - {factiva_message['description']}")
            else:
                print_message(f"[ERROR] Factiva Event Type Not Handled: {factiva_message['event_type']}")
                
        else:
            print_message(f"[ERROR] Unexpected Message Format:[{factiva_message}]")
            
        callback.counter += 1
        if callback.counter % 100 == 0:
            print_message(f"[INFO] *** Processed {callback.counter} messages ***")
                
    except Exception as e:
        print_message(f"[ERROR] Error processing Factiva message: {e}")
        # Only return False if you want to stop the listener
        return True
    return True

callback.counter = 0
listener_controller = listener.listen_async_ha(callback)

# Stop receiving messages after max_secs
for count in range(0, max_secs):
    sleep(1)

if listener_controller.listener_is_running():
    listener_controller.stop_listener()

print("stop receiving messages")
