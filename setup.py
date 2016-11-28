#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='dj-dna-streaming-python',
    version='0.9.1',
    description='Dow Jones DNA Streaming Project',
    author='Chris Flesche',
    author_email='chris.flesche@dowjones.com',
    url='https://github.dowjones.net/syndicationhub/dj-dna-streaming-python/',
    packages=find_packages(),

    package_data={
      # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst']
    },

    # metadata for upload to PyPI
    license="PSF",

    # could also include long_description, download_url, classifiers, etc.
    )