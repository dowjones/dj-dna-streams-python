import os
import json
import datetime
from google.cloud import pubsub_v1
from dnaStreaming.listener import Listener
from dnaStreaming import logger

gcp_project_id = os.getenv('GCP_PROJECT_ID', None)
gcp_pubsub_topic = os.getenv('GCP_PUBSUB_TOPIC', None)
gcp_creds = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', None)

def print_message(message):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

if gcp_project_id is not None and gcp_pubsub_topic is not None and gcp_creds is not None:
    listener = Listener()
    ps_publisher = pubsub_v1.PublisherClient()
    topic_path = ps_publisher.topic_path(gcp_project_id, gcp_pubsub_topic)
    print(f"\n[ACTIVITY] Sending messages to Pub/Sub topic {gcp_pubsub_topic} in GCP...")

    def callback(factiva_message, subscription_id, file_handle=None):
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
                    print_message(f"Factiva Action Not Handled: {factiva_message['action']}")
                
                logger.info(f"Sent to GCP Pub/Sub, message with AN: {factiva_message.get('an', 'N/A')}")
                
            elif 'event_type' in factiva_message.keys():
                # Message is a bulk action or service event
                if factiva_message['event_type'] == 'source_delete':
                    # Delete all articles from the repository matching the source_code. Handle inexistent source_code and repeated messages.
                    print_message(f"[EVENT] [SOURCE_DELETE] Source: {factiva_message['source_code'].upper()} - {factiva_message['description']}")
                else:
                    print_message(f"Factiva Event Type Not Handled: {factiva_message['event_type']}")

                logger.info(f"Sent to GCP Pub/Sub, message with event: {factiva_message.get('event_type', 'N/A')}")
                
            else:
                print_message(f"Unexpected Message Format:[{factiva_message}]")
                
            # Publish the message to GCP Pub/Sub
            m_data = json.dumps(factiva_message, ensure_ascii=False).encode("utf-8")
            ps_publisher.publish(topic_path, data=m_data)
            
            callback.counter += 1
        
            if callback.counter % 100 == 0:
                print_message(f"[INFO] *** Processed {callback.counter} messages ***")
                
            return True
        
        except Exception as e:
            logger.error(f"Error processing Factiva message: {e}")
            # Only return False if you want to stop the listener
            return True

    callback.counter = 0
    print_message(f"[INFO] *** Processed {callback.counter} messages ***")
    listener.listen(callback)
    
else:
    print("[ERROR]: Required ENV variables not set")
    if gcp_project_id is None:
        print("    - GCP_PROJECT_ID: GCP Project ID")
    if gcp_pubsub_topic is None:
        print("    - GCP_PUBSUB_TOPIC: GCP Pub/Sub Topic Name")
    if gcp_creds is None:
        print("    - GOOGLE_APPLICATION_CREDENTIALS: Path to Service Account JSON Credentials File")
