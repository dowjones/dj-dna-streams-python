# dj-dna-streaming-javascript
========================================

DNA Streaming Client - written in Python
----------------------------------------

How To Use
----------
This library is for Dow Jones customers consuming a Dow Jones DNA stream.

To use this we recommend 'pip installing' this by making the following addition to your requirements.txt:

.. code-block::

git+ssh://git@github.com/dowjones/dj-dna-streams-python#egg=dj-dna-streams-python

.. code-block::

Configuring

    To run this code, you need to provide both your 'service account ID' and your subscriptions. There are 3 ways to do this. You can either set environment variables or you can use a configuration file.

    1. Set environment variables.

        To set your service account ID, set an environment variable named 'SERVICE_ACCOUNT_ID' to your service account ID.
        To set your subscription IDS, set an environment variable named 'SUBSCRIPTION_IDS' to a comma delimited string like so:

            export SUBSCRIPTION_IDS="ABC1234567889, DEF9876543210"

            To be clear, the code above is the command line expression for setting this environment variable on Mac OSX. Other operating systems might have a slightly different techniques for setting environment variables on the command line. But pay close attention to how the subscription IDs are set with "ABC1234567889, DEF9876543210".

    2. Using the configuration file.

        In this codebase you will find a file named 'customer_config.json'. You are not required to use this file. If you prefer to use this configuration file, follow these directions: Open this file and add your service account ID. Then add your subscription IDs. Remember that this is a JSON file so follow basic JSON formatting and syntax conventions.

    3. Pass in variables as function arguments.

        To pass in service_account_id as a parameter value, you may pass account ID to the Listener constructor like so:

.. code-block::

            from dnaStreaming.listener import Listener

            listener = Listener(service_account_id='<YOUR ACCOUNT ID HERE>')

            def callback(message, subscription_id):
                print('Subscription ID: {}: Message: {}'.format(subscription_id, message.data.__str__()))
                return True  # If desired return False to stop the message flow. This will unblock the process as well.

            listener.listen(callback, maximum_messages=10)  # Omitting maximum_messages means you will continue to get messages as they appear. Can be a firehose. Use with caution.

.. code-block::

        Remember that passing account ID in this way will override the account ID environment variable and the config file setting.

        To pass subscription IDs as a parameter, you may pass subscription ID like like so:

.. code-block::

            from dnaStreaming.listener import Listener

            listener = Listener()

            def callback(message, subscription_id):
                print('Subscription ID: {}: Message: {}'.format(subscription_id, message.data.__str__()))
                return True  # If desired return False to stop the message flow. This will unblock the process as well.

            listener.listen(callback, maximum_messages=10, subscription_id='<YOUR SUBSCRIPTION ID HERE>')  # Omitting maximum_messages means you will continue to get messages as they appear. Can be a firehose. Use with caution.

.. code-block::

        Remember that passing subscription ID(s) in this way will override the subscription IDs environment variable and the config file setting.

Running the Demonstration Code

    If you have a account service account ID and a subscription ID you can run the demo code! Take your service account ID and subscription ID(s) abd follow the steps above in the 'Configuring' section above. Then follow these steps:

        i. At the command prompt, change to the project root directory.

        ii. Install the library like so:

                python setup.py install

        ii. Then execute the follow on the command line:

                python dnaStreaming/demo/show_stream.py

Testing
_______

.. code-block::

cd dnaStreaming/tests
pip install -r requirements.txt
py.test . -s

.. code-block::


Flake8
______

If you are maintaining this library, ensure you run flake8 before you commit. At project root command line:

.. code-block::

flake8 ./dnaStreaming ./tests

.. code-block::
