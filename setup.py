from distutils.core import setup

from setuptools import find_packages

setup(
    name='dj-dna-streaming-python',
    version='1.0.4',
    description='Dow Jones DNA Streaming Project',
    author='Chris Flesche',
    author_email='chris.flesche@dowjones.com',
    url='https://github.com/dowjones/dj-dna-streams-python',
    packages=find_packages(exclude='tests'),

    # metadata for upload to PyPI
    license="MIT",

    include_package_data=True,

    install_requires=[
        'google-api-python-client==1.6.2',
        'google-cloud-core==0.21.0',
        'google-cloud-pubsub==0.21.0',
        'mock==2.0.0',
        'requests==2.13.0'
    ]
)
