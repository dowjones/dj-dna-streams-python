import requests
import time

from dnaStreaming import logger

MAIN_REGION = "us-central1"
BACKUP_REGION = "us-east5"
COOLDOWN_PERIOD = 5 * 60

def get_active_region(api_host, subscription_id, user_key):

    try:
        ha_status_url = f"{api_host}/stream_health/get_active_region"

        headers = {
            "subscription-id": subscription_id,
            "user-key": user_key
        }

        response = requests.get(url=ha_status_url, headers=headers)

        assert response.status_code == 200, "Failed to fetch active region"

        payload = response.json()

        active_region = payload["data"]["active_region"]

        return active_region

    except:

        return None


def ha_listen(api_host, user_key, subscription_id, stop_event, main_subscription_path, backup_subscription_path, main_pubsub_client, backup_pubsub_client, callback):

    # The listener starts reading messages from the main region by default.

    current_region = MAIN_REGION

    def wrapped_callback(subscription_path):
        def inner_callback(message):
            callback(message, subscription_path)

        return inner_callback

    streaming_pull_future = main_pubsub_client.subscribe(
        main_subscription_path, callback=wrapped_callback(main_subscription_path))
    
    while not stop_event.is_set():

        active_region = get_active_region(api_host, subscription_id, user_key)

        if active_region is None or active_region not in (MAIN_REGION, BACKUP_REGION):
            logger.warning(f"Got invalid region from API: {active_region}. Listener will keep reading from region {current_region}")
            continue
        
        if current_region != active_region:

            logger.warning(f"Switch event detected in, switching from region {current_region} to region {active_region}")
            
            logger.warning(f"Stopping listener in region {current_region}...")

            # We stop the previous listening process
            streaming_pull_future.cancel()
            streaming_pull_future.result()

            logger.warning(f"Stopped listener in region {current_region}")

            logger.warning(f"Starting listener in region {active_region}...")

            if active_region == MAIN_REGION:
                streaming_pull_future = main_pubsub_client.subscribe(
                    main_subscription_path, callback=wrapped_callback(main_subscription_path))
            else: # active_region == BACKUP_REGION
                streaming_pull_future = backup_pubsub_client.subscribe(
                    backup_subscription_path, callback=wrapped_callback(backup_subscription_path))
                
            logger.warning(f"Started listener in region {active_region}")

            current_region = active_region
        
        # We wait 5 minutes for cooldown for next call to API
        time.sleep(COOLDOWN_PERIOD)

    streaming_pull_future.cancel()
    streaming_pull_future.result()
