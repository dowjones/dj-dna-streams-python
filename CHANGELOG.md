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
