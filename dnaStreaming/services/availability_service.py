import requests
import time

from dnaStreaming import logger

MAIN_REGION = "us-central1"
BACKUP_REGION = "us-east5"

def get_active_region(api_host):

    try:
        ha_status_url = f"{api_host}/stream_health/get_active_region"

        response = requests.get(ha_status_url)

        assert response.status_code == 200, "Failed to fetch active region"

        payload = response.json()

        active_region = payload["data"]["active_region"]

        return active_region

    except:

        return None


def ha_listen(api_host, stop_event, main_subscription_path, backup_subscription_path, main_pubsub_client, backup_pubsub_client, callback):

    # The listener starts reading messages from the main region by default.

    current_region = MAIN_REGION

    streaming_pull_future = main_pubsub_client.subscribe(
            main_subscription_path, callback=callback)
    
    while not stop_event.is_set():

        active_region = get_active_region(api_host)

        if active_region is None or active_region not in (MAIN_REGION, BACKUP_REGION):
            logger.warning(f"Got invalid region from API: {active_region}. Listener will keep reading from region {current_region}")
            continue
        
        if current_region != active_region:

            logger.warning(f"Regional indicent detected in {current_region}, switching to region {active_region}")
            
            logger.warning(f"Stopping listener in region {current_region}...")

            # We stop the previous listening process
            streaming_pull_future.cancel()
            streaming_pull_future.result()

            logger.warning(f"Stopped listener in region {current_region}")

            logger.warning(f"Starting listener in region {active_region}...")

            if active_region == MAIN_REGION:
                streaming_pull_future = main_pubsub_client.subscribe(
                    main_subscription_path, callback=callback)
            else: # active_region == BACKUP_REGION
                streaming_pull_future = backup_pubsub_client.subscribe(
                    backup_subscription_path, callback=callback)
                
            logger.warning(f"Started listener in region {current_region}")

            current_region = active_region
        
        # We wait 5 minutes for cooldown for next call to API
        time.sleep(5.0 * 60)

    streaming_pull_future.cancel()
    streaming_pull_future.result()
