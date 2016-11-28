#!/usr/bin/env python

from distutils.core import setup

setup(
    name='dnaStreaming',
    version='0.9.1',
    description='Dow Jones DNA Streaming Project',
    author='Chris Flesche',
    author_email='chris.flesche@dowjones.com',
    url='https://github.dowjones.net/syndicationhub/dj-dna-streaming-python/',
    packages=['subscriber'],
    package_dir={'subscriber':'lib'},

    # metadata for upload to PyPI
    license="PSF",

    install_requires=[
        "google-cloud-pubsub >= 0.21.0",
        "mock == 2.0.0",
    ]
    # could also include long_description, download_url, classifiers, etc.
    )