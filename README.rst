How To Use
----------

This a Python3 library is for Dow Jones customers consuming data from a Dow Jones Factiva Stream.

To use this we recommend 'pip installing' this please see below for more details.

Auth
-----------

Using the API user key.


Configuring
___________

To run this code, you need to provide credentials from one of the authentication methods and your subscriptions. There are 3 ways to do this. You can either set environment variables or you can use a configuration file.

1. Set environment variables.
###################################################################

To set your service account credentials, set:

- An environment variable named 'USER_KEY'

.. code-block::

    export USER_KEY="abcd1234abcd1234abcd1234abcd1234"

- A subscription ID by setting an environment variable named 'SUBSCRIPTION_ID'

.. code-block::

    export SUBSCRIPTION_ID="dj-synhub-stream-vxyz0987vxyz0987vxyz0987vxyz0987-4uu7uu4uu7-filtered-TmmSmmT"


The code above is the command line expression for setting this environment variable on Linux and Mac OSX. Other operating systems might have a slightly different techniques for setting environment variables on the command line.

2. Using the configuration file.
###################################################################

In this codebase you will find a file named 'customer_config.json'. You are not required to use this file. If you prefer to use this configuration file, follow these directions: Open this file and add your service account credentials. Then add your subscription IDs. Remember that this is a JSON file so follow basic JSON formatting and syntax conventions.

3. Pass in variables as function arguments.
###################################################################

You may pass your service account credentials (user_id, client_id, and password) to the Listener constructor like so:

.. code-block:: python

    from dnaStreaming.listener import Listener
    # User key authentication
    listener = Listener(user_key=<YOUR USER KEY>)

Or you may use the environment variables.
Remember that passing credentials and subscription ID(s) in this way will override the environment variable and the config file settings.

.. code-block:: python

    from dnaStreaming.listener import Listener

    listener = Listener()


4. Listening to messages
###################################################################

You may want to listen messages synchronously like so:

.. code-block:: python

    def callback(message):
        print('Message: {}'.format(message.data.__str__()))
        return True  # If desired return False to stop the message flow. This will unblock the process as well.

    listener.listen(callback, maximum_messages=10)  # Omitting maximum_messages means you will continue to get messages as they appear. Can be a firehose. Use with caution.
    # You may pass subscription ID as a parameter to the listen function


You may want to listen messages asynchronously like so:

.. code-block:: python

    def callback(message):
        print('Message: {}'.format(message.data.__str__()))

    future = listener.listen_async(callback)
    # After calling `listed_async` you need to keep the main thread alive.

    for count in range(0, 5):
        sleep(1)

    # Stop receiving messages after 5 seconds
    if future.running():
        future.cancel()


Log Files
_________

Very minimal logging is written to the module's path 'logs/dj-dna-streaming-python.log'. To keep maintenance simple this log is overwritten every time the app starts.


Testing
_______

.. code-block::

    cd dnaStreaming/test
    pip install -r requirements.txt
    py.test . -s


or, alternatively, to test against python2.7 and python3.5:

.. code-block::

    tox


Flake8
______

If you are maintaining this library, ensure you run flake8 before you commit. At project root command line:

.. code-block::

    flake8 ./dnaStreaming ./tests


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


4. Then activate the virutal environment by executing this command:
###################################################################

.. code-block::

    source ./venv/bin/activate


5. Install the App:
###################################################################

Production Environment: Copies the application as a package in a special location within the just created Python environment. In case the code is changed, the package has to be reinstalled.

.. code-block::

    pip install .

Development Environment: Uses the source files from the local folder. In case the code is changed, changes will be visible at the next execution.

.. code-block::

    pip install -e .


6. Set the Configuration Variables
###################################################################

See the config section.

7. Run the Demo Code
###################################################################

Running Non-Docker Demo:

Execute the following at the project root:

.. code-block::

    python ./dnaStreaming/demo/show_stream.py -s


Or

.. code-block::

    python ./dnaStreaming/demo/show_stream_async.py -s


If you are having `ImportError:  No module named ...` run this in your terminal before running the demo:

.. code-block::

    export PYTHONPATH='.'


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

or:

.. code-block::

    docker run -it \                    
    -e USER_KEY=<your user KEY> \
    -e SUBSCRIPTION_ID=<your subscription ID> \
    dj-dna-streaming-python
