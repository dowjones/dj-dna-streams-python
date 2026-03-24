from __future__ import absolute_import, division

import errno
import json
import os
from pathlib import Path


class Config(object):
    DEFAULT_HOST = "https://api.dowjones.com"

    DEFAULT_CUST_CONFIG_PATH = str(Path.home()) + "/customer_config.json"
    ENV_VAR_SUBSCRIPTION_ID = "SUBSCRIPTION_ID"
    ENV_VAR_USER_KEY = "USER_KEY"
    ENV_VAR_SERVICE_ACCOUNT_ID = "SERVICE_ACCOUNT_ID"
    ENV_VAR_OAUTH_TOKEN = "OAUTH_TOKEN"
    ENV_VAR_API_HOST = "API_HOST"

    def __init__(
        self, service_account_id=None, user_key=None, oauth_token=None, config_file=None
    ):
        self.customer_config_path = (
            self.DEFAULT_CUST_CONFIG_PATH if config_file is None else config_file
        )
        self.initialized = False
        self.service_account_id = service_account_id
        self.user_key = user_key
        self.oauth_token = oauth_token

        self.headers = None

    def _initialize(self):
        self._validate()

        with open(self.customer_config_path, "r") as f:
            self.customer_config = json.load(f)

        self.initialized = True
        self.headers = None

    def _validate(self):
        if not os.path.isfile(self.customer_config_path):
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), self.customer_config_path
            )

        if not os.access(self.customer_config_path, os.R_OK):
            raise Exception(
                "Encountered permission problem reading file from path '{}'.".format(
                    self.customer_config_path
                )
            )

    def get_headers(self):
        if self.headers:
            return self.headers
        else:
            self.headers = self.get_authentication_headers()
            return self.headers

    def get_authentication_headers(self):

        user_key = self.get_user_key()
        oauth_token = self.get_oauth_token()
        if oauth_token:
            return {"Authorization": f"Bearer {oauth_token}"}
        elif user_key:
            # TODO: deprecate user key
            return {"user-key": user_key}
        else:
            # TODO: deprecate user key
            msg = f"""
                Unable to find credentials. Please specify your account credentials using one of the following methods:
                - Set your user key as an environment variable named '{self.ENV_VAR_USER_KEY}'.
                - Set your OAuth token as an environment variable named '{self.ENV_VAR_OAUTH_TOKEN}'.
                - Set the `user_key` property inside your customer_config.json config file (refer to README.rst for more details).
                - Set the `oauth_token` property inside your customer_config.json config file (refer to README.rst for more details).
                - Pass the `user_key` parameter to the dnaStreaming.listener.Listener class constructor.
                - Pass the `oauth_token` parameter to the dnaStreaming.listener.Listener class constructor.
            """
            raise Exception(msg)

    def get_uri_context(self):
        host = os.getenv(self.ENV_VAR_API_HOST, self.DEFAULT_HOST)
        return host

    def get_oauth_token(self):

        potential_oauth_token_var = lambda: self.oauth_token
        potential_oauth_token_env = lambda: os.getenv(self.ENV_VAR_OAUTH_TOKEN)
        potential_oauth_token_from_file = lambda: self._oauth_token_from_file()

        potentials = [
            potential_oauth_token_var,
            potential_oauth_token_env,
            potential_oauth_token_from_file,
        ]

        # Lazily try to retrieve the value of the oauth token from all possible places where it may be set.
        oauth_token = next(
            (token for potential in potentials if (token := potential()) is not None),
            None,
        )

        return oauth_token

    # in the following two methods, note that we use "SERVICE_ACCOUNT_ID" as a legacy,
    # alternate name for the "USER_KEY" parameter, from the customer's perspective
    def get_user_key(self):

        potential_user_key_var = lambda: self.user_key
        potential_service_account_id_var = lambda: self.service_account_id
        potential_user_key_env = lambda: os.getenv(self.ENV_VAR_USER_KEY)
        potential_service_account_id_env = lambda: os.getenv(
            self.ENV_VAR_SERVICE_ACCOUNT_ID
        )
        potential_user_key_from_file = lambda: self._user_key_id_from_file()

        potentials = [
            potential_user_key_var,
            potential_service_account_id_var,
            potential_user_key_env,
            potential_service_account_id_env,
            potential_user_key_from_file,
        ]

        # Lazily try to retrieve the value of the user key from all possible places where it may be set.
        user_key = next(
            (key for potential in potentials if (key := potential()) is not None), None
        )

        return user_key

    def _user_key_id_from_file(self):
        if not self.initialized:
            self._initialize()

        return self.customer_config.get(
            "user_key", self.customer_config.get("service_account_id")
        )

    def subscription(self):
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

        return self.customer_config["subscription_id"]

    def _oauth_token_from_file(self):
        if not self.initialized:
            self._initialize()

        return self.customer_config.get("oauth_token")
