import time
import requests
import json
from google.api_core.exceptions import GoogleAPICallError, NotFound
from google import pubsub_v1
from threading import Thread

from dnaStreaming import logger
from dnaStreaming.config import Config
from dnaStreaming.services import pubsub_service, credentials_service


class Listener(object):
    DEFAULT_UNLIMITED_MESSAGES = None

    def __init__(self, service_account_id=None, user_key=None, user_id=None, client_id=None, password=None):
        config = Config(service_account_id, user_key, user_id, client_id, password)
        self._initialize(config)
        self.current_subscription_index = 0

    def _initialize(self, config):
        self.config = config

    # def _check_exceeded(self, subscription_id):
    #     host = self.config.get_uri_context()
    #     headers = self.config.get_headers()
    #     while True:
    #         stream_id_uri = host + '/streams/' + "-".join(subscription_id.split("-")[:-2])

    #         r = requests.get(stream_id_uri, headers=headers)

    #         try:
    #             if r.json()['data']['attributes']['job_status'] == "DOC_COUNT_EXCEEDED":
    #                 if "Authorization" in headers:
    #                     limits_uri = host + '/accounts/' + self.config.oauth2_credentials()['client_id']
    #                 else:
    #                     limits_uri = host + '/accounts/' + self.config.get_user_key()
    #                 limit_msg = 'NA'
    #                 try:
    #                     lr = requests.get(limits_uri, headers=headers)
    #                     limit_msg = lr.json()['data']['attributes']['max_allowed_extracts']
    #                 except KeyError:
    #                     logger.error('Could not parse account limit request response.')
    #                 logger.error(
    #                     'OOPS! Looks like you\'ve exceeded the maximum number of documents received for your account ' +
    #                     '({}). As such, no new documents will be added to your stream\'s queue. However, you won\'t ' +
    #                     'lose access to any documents that have already been added to the queue. These will continue ' +
    #                     'to be streamed to you. Contact your account administrator with any questions or to upgrade ' +
    #                     'your account limits.'.format(limit_msg))

    #         except KeyError:
    #             raise Exception(
    #                 "Unable to request data from your stream subscription id")
    #         time.sleep(5 * 60)

    # def check_exceeded_thread(self, subscription_id):
    #     thread = Thread(target=self._check_exceeded, args=[subscription_id])
    #     thread.start()

    def listen(self, on_message_callback, maximum_messages=DEFAULT_UNLIMITED_MESSAGES, subscription_id="", batch_size=10):
        pubsub_client = pubsub_service.get_client(self.config)

        subscription_id = subscription_id or self.config.subscription()
        if not subscription_id:
            raise Exception(
                'No subscription specified. You must specify the subscription ID either through an environment ' +
                'variable, a config file or by passing the value to the method.')

        # Possibly causing a high volume of requests in some circumstances, randomely triggering an error on the server side.
        # Also, fixes the freeze condition when the process is finished.
        # self.check_exceeded_thread(subscription_id)

        streaming_credentials = credentials_service.fetch_credentials(self.config)
        subscription_path = pubsub_client.subscription_path(streaming_credentials['project_id'], subscription_id)

        logger.info('Listeners for subscriptions have been configured, set and await message arrival.')

        count = 0
        while maximum_messages is None or count < maximum_messages:
            try:
                if maximum_messages is not None:
                    batch_size = min(batch_size, maximum_messages - count)

                pull_request = pubsub_v1.PullRequest(
                                   subscription=subscription_path,
                                   max_messages=batch_size,
                               )
                results = pubsub_client.pull(request=pull_request)
                # results = pubsub_client.pull(subscription=subscription_path, max_messages=batch_size) #, return_immediately=True)
                if results:
                    if len(results.received_messages) > 0:
                        for message in results.received_messages:
                            pubsub_msg = json.loads(message.message.data)
                            logger.info("Received news message with ID: {}".format(pubsub_msg['data'][0]['id']))
                            news_msg = pubsub_msg['data'][0]['attributes']
                            callback_result = on_message_callback(news_msg)
                            if callback_result:
                                ack_request={
                                    "subscription": subscription_path,
                                    "ack_ids": [message.ack_id],
                                }
                                pubsub_client.acknowledge(request=ack_request)
                                # pubsub_client.acknowledge(subscription_path, [message.ack_id])
                            else:
                                logger.error('Callback function returned False.')
                                return
                            count += 1


            except GoogleAPICallError as e:
                if isinstance(e, NotFound):
                    raise e
                logger.error("Encountered a problem while trying to pull a message from a stream. Error is as follows: {}".format(str(e)))
                logger.error("Due to the previous error, system will pause 10 seconds. System will then attempt to pull the message from "
                             "the stream again.")
                time.sleep(10)
                pubsub_client = pubsub_service.get_client(self.config)

    def listen_async(self, on_message_callback, subscription_id=""):
        def ack_message_and_callback(message):
            pubsub_msg = json.loads(message.data)
            logger.info("Received news message with ID: {}".format(pubsub_msg['data'][0]['id']))
            news_msg = pubsub_msg['data'][0]['attributes']
            on_message_callback(news_msg, subscription_id)
            message.ack()

        pubsub_client = pubsub_service.get_client(self.config)

        subscription_id = subscription_id or self.config.subscription()

        if not subscription_id:
            raise Exception(
                'No subscription specified. You must specify the subscription ID either through an environment variable, a config file or '
                'by passing the value to the method.')

        # self.check_exceeded_thread(subscription_id)

        streaming_credentials = credentials_service.fetch_credentials(self.config)
        subscription_path = pubsub_client.subscription_path(streaming_credentials['project_id'], subscription_id)
        subscription = pubsub_client.subscribe(subscription_path, callback=ack_message_and_callback)
        logger.info('Listeners for subscriptions have been configured, set and await message arrival.')
        return subscription
