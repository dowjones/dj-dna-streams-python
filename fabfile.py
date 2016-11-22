import logging
import os
from contextlib import contextmanager
from fabric.api import *

logging.basicConfig(filename='logs/app.log', level=logging.WARNING)
logger = logging.getLogger(__name__)

env.directory = os.path.dirname(os.path.realpath(__file__))
env.activate = 'source ' + env.directory + '/venv/bin/activate' # use virtual environment to execute commands

@contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield

def call( cmd):
    local( cmd, shell="/bin/bash")

def install_reqs():
    with virtualenv():
        call("pip install -r requirements.txt")