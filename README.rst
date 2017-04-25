# dj-dna-streaming-javascript
========================================

DNA Streaming Client - written in Python
----------------------------------------

How To Use
----------
This library is for Dow Jones customers consuming a Dow Jones Snapshot as a stream.

To use this we recommend pip installing this by making the following addition to your requirements.txt:

.. code-block::

git+ssh://git@github.dowjones.net/syndicationhub/dj-dna-streaming-python#egg=dj-dna-streaming-python

.. code-block::


When executing code that invokes this module ensure you have set the following environment variable -- DOW_JONES_JSON_CONFIG_PATH

.. code-block:: DOW_JONES_JSON_CONFIG_PATH

DOW_JONES_JSON_CONFIG_PATH: This environment variable should hold the file path of your Dow Jones provided security json file (e.g., 'DowJonesDNA.json').


Testing
_______

Before you run your test, add your Dow Jones DNA JSON (DowJonesDNA.json) file to the 'tests' directory.

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
