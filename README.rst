# dj-dna-streaming-javascript
========================================

DNA Streaming Client - written in Python
----------------------------------------

How To Use
----------
This library is for Dow Jones customers consuming a Dow Jones DNA stream.

To use this we recommend pip installing this by making the following addition to your requirements.txt:

.. code-block::

git+ssh://git@github.dowjones.net/syndicationhub/dj-dna-streaming-python#egg=dj-dna-streaming-python

.. code-block::

Configuring

    To run this code, you need to provide both your 'service account ID' and your subscriptions. There are 2 ways to do this. You can either set environment variables or you can use a configuration file.

    1. Set environment variables.

        To set your service account ID, set an environment variable named 'SERVICE_ACCOUNT_ID' to your service account ID.
        To set your subscription IDS, set an environment variable named 'SUBSCRIPTION_IDS' to a comma delimited string like so:

            export SUBSCRIPTION_IDS="ABC1234567889, DEF9876543210"

            To be clear, the code above is the command line expression for setting this environment variable on Mac OSX. Other operating systems might have a slightly different techniques for setting environment variables on the command line. But pay close attention to how the subscription IDs are set with "ABC1234567889, DEF9876543210".

    2. Using the configuration file.

        In this codebase you will find a file named 'customer_config.json'. Open this file and add your service account ID. Then add your subscription IDs. Remember that this is a JSON file so follow basic JSON formatting and syntax conventions.

Running the Demonstration

If you have a account service account ID and a subscription ID you can run the demo code! Take your service account ID and subscription ID(s) abd follow the steps above in the 'Configuring' section above. Then follow these steps:

    i. At the command prompt, change to the project root directory.

    ii. Execute the follow on the command line:

            python src/show_stream.py

Testing
_______

.. code-block::

cd tests
pip install -r requirements.txt
py.test . -s

.. code-block::


Flake8
______

If you are maintaining this library, ensure you run flake8 before you commit. At project root command line:

.. code-block::

flake8 ./dnaStreaming ./tests

.. code-block::
