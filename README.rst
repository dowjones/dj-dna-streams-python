# dj-dna-streaming-javascript
=============================

DNA Streaming Client - written in Python
----------------------------------------

How To Use
----------

Installing
----------

Install this at your project root by invoking the following command line:

.. code-block::

 
 or 

.. code-block::


Add Code to Subscribe to a DNA Topic or Two
-------------------------------------------

.. code-block::


Execute with Environment Variables
---------------------------------------

When executing code that invokes this module ensure you have set the following environment variables -- GOOGLE_CLOUD_AUTHENTICATION, SUBSCRIBER_NAME and (optionally) GCLOUD_PROJECT.

.. code-block:: GOOGLE_CLOUD_AUTHENTICATION

GOOGLE_CLOUD_AUTHENTICATION: This environment variable should hold the file path of your Dow Jones provided security json file (googleApplicationCredentials.json).

.. code-block:: SUBSCRIBER_NAME

SUBSCRIBER_NAME: Set this environment variable to your Dow Jones provided subscriber name.

.. code-block:: GCLOUD_PROJECT (optional)

GCLOUD_PROJECT: Most users will not need to use this variable. If you do not set this environment variable the code will use the default Dow Jones DNA Google Cloud production project name.

.. code-block:: Example Execution Command (MacOS)


