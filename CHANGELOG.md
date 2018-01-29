0.9.2 / 2017-04-14
==================
- [docs] Updated README.rst. 
- [breaking] Removed subscriber module. Added 'listener'. This will simplify how customers run our code. No longer will they be creating
the subscription *and* consuming it. Instead they will just consume an already existing subscription.
- [Tests] Updated tests to use listener. Updated tests to use new name for sample credentials file. Deleted old subscriber test.

0.9.3 / 2017-04-25
==================
- [docs] Updated README.rst
- [breaking] Replaced references 'DOW_JONES_APPLICATION_CREDENTIALS' envinronmental variable for 'DOW_JONES_DNA_JSON_PATH'.
- [breaking] Replaced system's filename expectation for 'dowJonesApplicationCredentials.json' to 'DowJonesDNA.json':
- [Tests] Updated test to use the changes described above.

1.0.0 / 2017-06-07
==================
- [docs] Updated README.rst
- [breaking] - No longer using 'DowJonesDNA.json' file.
- [changed] - Added customer_config.json file. See README.rst for usage explanation.
- [changed] - Get the user's credentials information by making a REST call to Dow Jones extraction API service.
- [Tests] Updated tests to use the changes described above.

1.0.1 / 2017-06-09
==================
- [breaking] Removed ability to consume more than one stream at a time.
- [tests] Updated tests.
- [docs] Updated README.

1.0.2 / 2017-06-29
==================
- [changed] - Reduced the listed dependencies in requirements.txt and setup.py.
- [changed] - Corrected URI in setup.py.
- [tests] Fixed 2 broken tests in test_config.py.
- [docs] Updated README with more complete instructions.

1.0.3 / 2017-06-29
==================
- [changed] - Changed default PROD URI.

1.0.4 / 2017-06-29
==================
- [docs] - Updated README. Git project pip install should use 'https'.

1.0.5 / 2017-08-02
==================
- [changed] - Added Google API Extension (GaxError) error handling. Adding a logging file that will catch logged information. Log name is 'logs/dj-dna-streaming-python.log'.
- [docs] - Updated README with information about logs.  

1.0.6 / 2017-08-04
==================
- [changed] - Fixed how we handle GaxErrors

1.0.7 / 2017-08-04
==================
- [changed] - Added tox tests to test against python2 and python3.
- [changed] - Made some python3 compatibility changes. 

1.0.8 / 2017-08-04
==================
- [changed] - Refactored how we do pull and acknowledge messages to be more clear. 

1.0.9 / 2017-08-17
==================
- [changed] - Created a Dockerfile for demo purposes.
- [docs] - Updated README.

1.0.10 / 2017-08-22
==================
- [changed] - Dependency now pulls in entire GCloud library due to compatibility concerns. Will revert back to more focused dependency list in the future.
- [changed] - Upgraded Google Cloud dependency version to fix incompatibility with Google language module in a related project.

1.0.11 / 2018-01-29
==================
- [changed] - Updated demo code to accept environment variable that, when used, reduces the output volume.
- [changed] - Added test shell script './dnaStreaming/test/test_run_docker.sh' for testing Docker and streams; to be used only with DNA Engineering assistance.  

