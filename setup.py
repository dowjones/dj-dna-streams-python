from distutils.core import setup
from setuptools import find_packages
# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = "2.1.0"
RELEASE_TAG = f"release-{VERSION}"

setup(
    name='dnaStreaming',
    version=VERSION,
    description='Dow Jones DNA Streaming Project',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Zachary Kagan',
    author_email='zachary.kagan@dowjones.com',
    url='https://github.com/dowjones/dj-dna-streams-python',
    download_url=f'https://github.com/dowjones/dj-dna-streams-python/archive/{RELEASE_TAG}.tar.gz',
    keywords=['DOWJONES', 'FACTIVA', 'STREAMS'],
    packages=find_packages(exclude='tests'),

    # metadata for upload to PyPI
    license="MIT",

    include_package_data=True,

    install_requires=[
        'googleapis-common-protos>=1.56.4',
        'google-auth>=2.11.0',
        'google-cloud-pubsub==2.13.6',
        'google-cloud-core==2.3.2',
        'google-api-core==2.10.1',
        'mock>=3.0.5',
        'oauth2client>=4.1.3',
        'requests>=2.28.0'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)
