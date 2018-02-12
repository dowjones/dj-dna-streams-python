dj-dna-streams-python
========================================

DNA Streaming Client - written in Python
----------------------------------------

How To Use
----------


This library is for Dow Jones customers consuming a Dow Jones DNA stream.

To use this we recommend 'pip installing' this by making the following addition to your requirements.txt:

.. code-block::

    git+https://git@github.com/dowjones/dj-dna-streams-python#egg=dj-dna-streams-python

.. code-block::

Configuring
___________

To run this code, you need to provide both your service account credentials and your subscriptions. There are 3 ways to do this. You can either set environment variables or you can use a configuration file.

1. Set environment variables.
###################################################################

To set your service account credentials, set three environment variable named 'USER_ID', 'CLIENT_ID', and 'PASSWORD'
To set your subscription IDS, set an environment variable named 'SUBSCRIPTION_IDS' to a comma delimited string like so:

.. code-block::

    export SUBSCRIPTION_IDS="ABC1234567889, DEF9876543210"

.. code-block::

To be clear, the code above is the command line expression for setting this environment variable on Mac OSX. Other operating systems might have a slightly different techniques for setting environment variables on the command line. But pay close attention to how the subscription IDs are set with "ABC1234567889, DEF9876543210".

2. Using the configuration file.
###################################################################

In this codebase you will find a file named 'customer_config.json'. You are not required to use this file. If you prefer to use this configuration file, follow these directions: Open this file and add your service account credentials. Then add your subscription IDs. Remember that this is a JSON file so follow basic JSON formatting and syntax conventions.

3. Pass in variables as function arguments.
###################################################################

You may pass your service account credentials (user_id, client_id, and password) to the Listener constructor like so:

.. code-block::

    from dnaStreaming.listener import Listener

    listener = Listener(user_id=<YOUR USER ID>, client_id=<YOUR_CLIENT_ID>, password=<YOUR_PASSWORD>)

    def callback(message, subscription_id):
        print('Subscription ID: {}: Message: {}'.format(subscription_id, message.data.__str__()))
        return True  # If desired return False to stop the message flow. This will unblock the process as well.

    listener.listen(callback, maximum_messages=10)  # Omitting maximum_messages means you will continue to get messages as they appear. Can be a firehose. Use with caution.
            You may pass subscription ID as a parameter to the listen function like so:

.. code-block::

You may pass your subcription ID as a parameter to the listen function like so:

.. code-block::

    from dnaStreaming.listener import Listener

    listener = Listener()

    def callback(message, subscription_id):
        print('Subscription ID: {}: Message: {}'.format(subscription_id, message.data.__str__()))
        return True  # If desired return False to stop the message flow. This will unblock the process as well.

    listener.listen(callback, maximum_messages=10, subscription_id='<YOUR SUBSCRIPTION ID HERE>')  # Omitting maximum_messages means you will continue to get messages as they appear. Can be a firehose. Use with caution.

.. code-block::

Remember that passing credentials and subscription ID(s) in this way will override the environment variable and the config file settings.

Log Files
_________

Very minimal logging is written to the module's path 'logs/dj-dna-streaming-python.log'. To keep maintenance simple this log is overwritten every time the app starts.


Testing
_______

.. code-block::

    cd dnaStreaming/test
    pip install -r requirements.txt
    py.test . -s

.. code-block::

or, alternatively, to test against python2.7 and python3.5:

.. code-block::

    tox

.. code-block::


Flake8
______

If you are maintaining this library, ensure you run flake8 before you commit. At project root command line:

.. code-block::

    flake8 ./dnaStreaming ./tests

.. code-block::


Running the Demonstration Code/Development
__________________________________________

If you are enhancing this codebase (and not just using it as a library), follow these example MacOS steps:

1. Checkout the Project from Git.
###################################################################

2. Go to the Project Root.
###################################################################

3. Create a Virtual Environment.
###################################################################

.. code-block::

    virtualenv venv

.. code-block::

4. Then activate the virutal environment by executing this command:
###################################################################

.. code-block::

    source ./venv/bin/activate

.. code-block::

5. Install the Dependencies
###################################################################

.. code-block::

    pip install -r requirements.txt

.. code-block::

6. Install the App:
###################################################################

.. code-block::

    python setup.py install

.. code-block::


7. Set the Configuration Variables
###################################################################

See the config section.

8. Run the Demo Code
###################################################################

Running Non-Docker Demo:

Execute the following at the project root:

.. code-block::

    python ./dnaStreaming/demo/show_stream.py -s

.. code-block::


Running Docker Demo

Execute the following at the project root:

.. code-block::

    docker build -f ./DockerfileDemo -t dj-dna-streaming-python .

    docker run -it \
    -e USER_ID=<your user ID> \
    -e CLIENT_ID=<your client ID> \
    -e PASSWORD=<your password> \
    -e SUBSCRIPTION_ID=<your subscription ID> \
    dj-dna-streaming-python

.. code-block::