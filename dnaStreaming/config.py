import json
import os


class Config(object):
    CRED_PROD_URI = 'https://api.dowjones.io/alpha/accounts/streaming-credentials'
    DEFAULT_CUST_CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), './customer_config.json'))
    ENV_VAR_SERVICE_ACCOUNT_ID = 'SERVICE_ACCOUNT_ID'
    ENV_VAR_SUBSCRIPTION_ID = 'SUBSCRIPTION_ID'
    ENV_VAR_CREDENTIALS_URI = 'CREDENTIALS_URI'

    def __init__(self, account_id=None):
        self.customer_config_path = self.DEFAULT_CUST_CONFIG_PATH
        self.initialized = False
        self.account_id = account_id

    def _initialize(self):
        self._validate()

        with open(self.customer_config_path, 'r') as f:
            self.customer_config = json.load(f)

        self.initialized = True

    def _validate(self):
        if not os.path.isfile(self.customer_config_path):
            raise Exception('Encountered problem finding \'customer_config.json\' at path \'{}\'. Does it exist?'.format(self.customer_config_path))

        if not os.access(self.customer_config_path, os.R_OK):
            raise Exception('Encountered permission problem reading file from path \'{}\'.'.format(self.customer_config_path))

    def service_account_id(self):
        service_account_id = None
        if self.account_id is not None:
            service_account_id = self.account_id
        else:
            service_account_id = os.getenv(self.ENV_VAR_SERVICE_ACCOUNT_ID)

            if service_account_id is None:
                service_account_id = self._service_account_id_from_file()

        return service_account_id

    def _service_account_id_from_file(self):
        if not self.initialized:
            self._initialize()

        return self.customer_config['service_account_id']

    def subscription(self):

        subscription = None
        if os.getenv(self.ENV_VAR_SUBSCRIPTION_ID) is not None:
            subscription = os.getenv(self.ENV_VAR_SUBSCRIPTION_ID)
        else:
            subscription = self._subscription_id_from_file()

        return subscription

    def _set_customer_config_path(self, path):
        self.customer_config_path = path
        self._initialize()

    def _subscription_id_from_file(self):
        if not self.initialized:
            self._initialize()

        return self.customer_config['subscription_id']

    def credentials_uri(self):
        return os.getenv(self.ENV_VAR_CREDENTIALS_URI, self.CRED_PROD_URI)
