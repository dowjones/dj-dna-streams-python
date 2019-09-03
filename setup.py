from distutils.core import setup

from setuptools import find_packages

setup(
    name='dj-dna-streaming-python',
    version='1.4.0',
    description='Dow Jones DNA Streaming Project',
    author='Chris Flesche',
    author_email='chris.flesche@dowjones.com',
    url='https://github.com/dowjones/dj-dna-streams-python',
    packages=find_packages(exclude='tests'),

    # metadata for upload to PyPI
    license="MIT",

    include_package_data=True,

    install_requires=[
        'googleapis-common-protos>=1.6.0',
        'google-auth>=1.6.0',
        'google-cloud-pubsub==0.38.0',
        'google-cloud-core==0.28.1',
        'mock==2.0.0',
        'oauth2client==3.0.0',
        'requests==2.20.1'
    ],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ]
)
