from distutils.core import setup

from setuptools import find_packages

setup(
    name='dj-dna-streaming-python',
    version='1.0.1',
    description='Dow Jones DNA Streaming Project',
    author='Chris Flesche',
    author_email='chris.flesche@dowjones.com',
    url='https://github.dowjones.net/syndicationhub/dj-dna-streaming-python/',
    packages=find_packages(exclude='tests'),

    # metadata for upload to PyPI
    license="PSF",

    include_package_data=True,

    install_requires=[
        'flake8==3.3.0',
        'google-api-python-client==1.6.2',
        'google-cloud-core==0.21.0',
        'google-cloud-pubsub==0.21.0',
        'mock==2.0.0',
        'pyflakes==1.5.0',
        'pytest==2.9.2',
        'pytest-cov==2.3.0',
        'pytest-mock==1.1',
        'requests==2.13.0'
    ]
    # could also include long_description, download_url, classifiers, etc.
)
