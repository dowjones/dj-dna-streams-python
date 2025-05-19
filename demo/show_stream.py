import os
import datetime
from dnaStreaming.listener import Listener

listener = Listener()

print("[ACTIVITY] Receiving messages (SYNC)...")


def print_message(message):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")


def callback(factiva_message: dict, subscription_id: str) -> bool:
    try:
        if 'action' in factiva_message.keys(): 
            # Message is an article event
            # Implement your logic according to the documentation:
            # https://developer.dowjones.com/documents/site-docs-factiva_apis-factiva_analytics_apis-factiva_streams_api#article-specific-events
            if factiva_message['action'] == 'add':
                # Insert the article to the repository as new. Handle repeated messages.
                print_message(f"[{factiva_message['action'].upper()}] AN: {factiva_message['an']} - {factiva_message['title']}")
            elif factiva_message['action'] == 'rep':
                # Upsert/Update/AddNewVersion the article in the repository. Handle repeated messages.
                print_message(f"[{factiva_message['action'].upper()}] AN: {factiva_message['an']} - {factiva_message['title']}")
            elif factiva_message['action'] == 'del':
                # Delete or mark as deleted the article in the repository. Handle inexistent article AN.
                print_message(f"[{factiva_message['action'].upper()}] AN: {factiva_message['an']} - *** DELETE ***")
            else:
                print_message(f"[ERROR] Factiva Action Not Handled: {factiva_message['action']}")

        elif 'event_type' in factiva_message.keys():
            # Message is a bulk action or service event
            if factiva_message['event_type'] == 'source_delete':
                # Delete all articles from the repository matching the source_code. Handle inexistent source_code and repeated messages.
                print_message(f"[{factiva_message['event_type'].upper()}] Source: {factiva_message['source_code'].upper()} - {factiva_message['description']}")
            else:
                print_message(f"[ERROR] Factiva Event Type Not Handled: {factiva_message['event_type']}")

        else:
            print_message(f"[ERROR] Unexpected Message Format:[{factiva_message}]")
    
    except Exception as e:
        print_message(f"[ERROR] Error processing Factiva message: {e}")
        # Only return False if you want to stop the listener
        return True

    return True


callback.counter = 0
listener.listen(callback)