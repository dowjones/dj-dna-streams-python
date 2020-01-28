from __future__ import absolute_import, division, print_function

import os
import sys
import logging


BASE_DIR = os.path.dirname(__file__)

logging.basicConfig(level=logging.WARN)

logger = logging.getLogger()

log_path = os.path.join(BASE_DIR, 'logs')

print("Will log to: {}".format(log_path))

if not os.path.exists(log_path):
    os.mkdir(log_path)

fileHandler = logging.FileHandler("{0}/{1}.log".format(log_path, 'dj-dna-streaming-python'))

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)
