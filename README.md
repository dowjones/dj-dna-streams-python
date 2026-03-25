# Dow Jones DNA Streaming Python Library

A Python 3 library for Dow Jones customers to consume data from a Factiva Analytics Stream.

## Installation

To use this, we recommend installing it via `pip` by making the following addition to your `requirements.txt`:

```text
# To fetch the latest version from PyPI
dnaStreaming

# To fetch the latest version from GitHub
git+https://github.com/dowjones/dj-dna-streams-python#egg=dnaStreaming
```

---

## Authentication

You have two options to authenticate:
- By using your **user key**
- By using an **OAuth bearer token** (new)

---

## Configuration

To run this code, you need to provide credentials from one of the authentication methods, as well as your subscriptions. There are three ways you can do this: 

### 1. Environment Variables

To set your credentials, set either `USER_KEY` or `OAUTH_TOKEN` as an environment variable:

```bash
export USER_KEY="<your_user_key>"
# or
export OAUTH_TOKEN="<your_oauth_bearer_token>"
```

To set your subscription ID, set an environment variable named `SUBSCRIPTION_ID`:

```bash
export SUBSCRIPTION_ID="ABC1234567889"
```

To set your log folder path, set a directory variable named `LOG_PATH`:

```bash
export LOG_PATH="/your/custom/log/path"
```

### 2. Configuration File

In this codebase, you will find a file named `customer_config.json`. You are not required to use this file, but if you prefer to, fill the JSON object within by adding your user key and your subscription ID. Follow basic JSON formatting and syntax conventions.

> **Note:** The listener will search for the `customer_config.json` file inside your `$HOME` directory by default.

If you prefer using an explicit path to your configuration file, pass the absolute path to the `Listener` constructor:

```python
from dnaStreaming.listener import Listener

# Config file authentication
listener = Listener(config_file="<ABSOLUTE_PATH_TO_YOUR_CONFIG_FILE>")
```

### 3. Function Arguments

You may pass your user key or OAuth token to the `Listener` constructor and your subscription ID directly to the `listen` method:

```python
from dnaStreaming.listener import Listener

# Use the user_key argument to provide your credentials
listener = Listener(user_key="<YOUR_USER_KEY>")

# Alternatively, use the oauth_token argument
listener = Listener(oauth_token="<YOUR_OAUTH_BEARER_TOKEN>")

# Use the subscription_id argument to provide your subscription id to the listener
listener.listen(callback, subscription_id="<YOUR_SUBSCRIPTION_ID>")

# The same parameter applies for the async variation
listener.listen_async(callback, subscription_id="<YOUR_SUBSCRIPTION_ID>")
```

*Note: Passing credentials and subscription ID(s) via function arguments will override both environment variables and config file settings.*

If you choose to strictly rely on environment variables, you can simply initialize the listener empty:

```python
from dnaStreaming.listener import Listener

listener = Listener()
```

---

## Listening to Messages

### Synchronous Listening

If you want to listen to messages synchronously:

```python
def callback(message, subscription_id):
    print(f'Subscription ID: {subscription_id}: Message: {message.data}')
    return True  # Return False to stop the message flow and unblock the process.

# Omitting maximum_messages means you will continue to get messages as they appear. 
# This can be a firehose. Use with caution.
listener.listen(callback, maximum_messages=10)  
```

### Asynchronous Listening

If you want to listen to messages asynchronously:

```python
from time import sleep

def callback(message, subscription_id):
    print(f'Subscription ID: {subscription_id}: Message: {message.data}')

future = listener.listen_async(callback)

# After calling `listen_async`, you need to keep the main thread alive.
for count in range(0, 5):
    sleep(1)

# Stop receiving messages after 5 seconds
if future.running():
    future.cancel()
```

---

## Log Files

Minimal logging is written to a file named `dj-dna-streaming-python.log`.

By default, logs are written to the first available directory from the following list:
1. A custom path set via the environment variable `LOG_PATH`.
2. A `logs/` folder located within the package installation directory.
3. A fallback directory: `~/.dj-dna-streaming-python/logs/`.

The first writable location found is selected. A message like `Will log to: /your/custom/log/path` is printed to the console on startup.

💡 **Note:** The log file is overwritten each time the application starts to keep maintenance simple.

You can specify:
- **Absolute paths**: For example, `/var/log/dna-streaming`.
- **Relative paths**: For example, `./logs`, relative to the current working directory at runtime.

The code verifies that the specified path is writable. If it isn’t, it automatically falls back to the next available option.

---

## Development, Testing & Linting (for developers)

### Setup

To prepare for local development and debugging, create a virtual environment and install
both runtime and dev dependencies (make sure to run with a recent version of Python 3):

```bash
python3 install -m venv env
source env/bin/activate
# Install runtime dependencies from pyproject.toml (-e for recommended editable install)
pip3 install -e .
# Install dev dependencies from pyproject.toml
pip3 install -e ".[dev]"
```

### Running Tests
To test the library works over multiple Python versions (e.g., Python >= 3.10), use `tox`:

```bash
# Make sure to set USER_KEY, API_HOST and SUBSCRIPTION_ID accordingly
# Strong recommendation:
#  - SUBSCRIPTION_ID should belong to an active stream with about 2000 queued messages
#    for faster test execution times.
tox
```

### Linting
Before releasing, or ideally, before you commit, make sure to `ruff` your code 
to align with minimal but recommended linting. At the project root, run:

```bash
ruff check . # checks code without changing it
ruff check --fix . # checks code and applies changes
ruff format . # formats code
```