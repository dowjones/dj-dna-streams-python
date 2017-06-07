from distutils.core import setup

setup(
    name='dj-dna-streaming-python',
    version='1.0.0',
    description='Dow Jones DNA Streaming Project',
    author='Chris Flesche',
    author_email='chris.flesche@dowjones.com',
    url='https://github.dowjones.net/syndicationhub/dj-dna-streaming-python/',
    packages=['dnaStreaming'],

    # metadata for upload to PyPI
    license="PSF",

    install_requires=[
        "google-cloud-pubsub >= 0.21.0",
        "mock == 2.0.0",
        "requests == 2.12.4"
    ]
    # could also include long_description, download_url, classifiers, etc.
    )
