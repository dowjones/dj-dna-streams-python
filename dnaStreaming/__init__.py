from __future__ import absolute_import, division, print_function

import os
import sys
import logging


def get_log_path():
    env_log_path = os.getenv("LOG_PATH")
    fallback_log_dir = os.path.expanduser('~/.dj-dna-streaming-python/logs')
    base_dir = os.path.dirname(__file__)
    default_path = os.path.join(base_dir, 'logs')

    candidates = [env_log_path, default_path, fallback_log_dir]

    for path in candidates:
        if path:
            try:
                os.makedirs(path, exist_ok=True)
                testfile = os.path.join(path, '.write_test')
                with open(testfile, 'w') as f:
                    f.write('test')
                os.remove(testfile)
                return path
            except Exception as e:
                print(f"WARNING: Cannot write to '{path}': {e}")

    raise RuntimeError("ERROR: Could not find a writable log directory.")


log_path = get_log_path()
print("Will log to: {}".format(log_path))

# Logging setup
logging.basicConfig(level=logging.WARN)
logger = logging.getLogger()

fileHandler = logging.FileHandler(os.path.join(log_path, 'dj-dna-streaming-python.log'))
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)
