import time
import logging
import pytest
from dnaStreaming.listener import Listener

logging.basicConfig(level=logging.INFO)

MIN_SAMPLE_SIZE = 100

listener = Listener()

# Sample articles fetched with sync listener
# to be used by all tests in this module
@pytest.fixture(scope="module", autouse=True)
def sample():
    # Destination for sample messages.
    sample_list = []
    # Minimal callback function to store sample messages inside a list.
    def callback(factiva_message: dict, subscription_id: str) -> bool:
        try:
            sample_list.append(factiva_message) 
            logging.info(f"*** Fetched {len(sample_list)} messages from subscription {subscription_id} ***")
            return True
        
        except Exception as e:
            logging.error(f"*** Error processing Factiva message: {e} ***")
            return False

    future = listener.listen_async(on_message_callback=callback)

    while len(sample_list) < MIN_SAMPLE_SIZE:
        logging.info("Sample is still too short, waiting for more articles to come.")
        time.sleep(1)

    if len(sample_list) < MIN_SAMPLE_SIZE:
        raise ValueError("Could not put together the sample of messages.")
    
    future.cancel()
    future.result()

    return sample_list
    
def test_sample_schema_async(sample):
    sample_has_factiva_messages = any(message.get("an") is not None for message in sample)
    assert sample_has_factiva_messages