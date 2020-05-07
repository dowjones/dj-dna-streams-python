from distutils.core import setup

from setuptools import find_packages

setup(
    name='djdp-streaming-python',
    version='1.5.0',
    description='Dow Jones DNA Streaming Project',
    author='Chris Flesche',
    author_email='chris.flesche@dowjones.com',
    url='https://github.com/miballe/dp-streams-python',
    packages=find_packages(exclude='tests'),

    # metadata for upload to PyPI
    license="MIT",

    include_package_data=True,

    install_requires=[
        'googleapis-common-protos>=1.6.0',
        'google-auth>=1.7.0',
        'google-cloud-pubsub>=1.0.0',
        'google-cloud-core>=1.0.3',
        'google-api-core<1.17.0,>=1.14.0'
        'mock>=3.0.5',
        'oauth2client>=4.1.3',
        'requests>=2.22.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3'
    ]
)
