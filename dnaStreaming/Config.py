import os
import json

class Config():

    GOOGLE_APPLICATION_CREDENTIALS = 'GOOGLE_APPLICATION_CREDENTIALS'
    DOW_JONES_CONFIG_KEY = 'dj_dna_streaming'

    def __init__(self):

        needsCredentials = not os.environ.has_key(self.GOOGLE_APPLICATION_CREDENTIALS)

        if (needsCredentials):
            raise Exception('Encountered problem reading required environmental variable \'{}\'. Did you set it the environment variable \'{}\' to the path of your Dow Jones provided security file?'.format(self.GOOGLE_APPLICATION_CREDENTIALS, self.GOOGLE_APPLICATION_CREDENTIALS))

        credentialsPath = os.environ[self.GOOGLE_APPLICATION_CREDENTIALS]

        if (not os.path.isfile(credentialsPath)):
            raise Exception('Encountered problem finding file at path \'{}\'. Does it exist?'.format(credentialsPath))

        if (not os.access(credentialsPath, os.R_OK)):
            raise Exception('Encountered permission problem reading file from path \'{}\'.'.format(credentialsPath))

        with open(credentialsPath, 'r') as f:
            self.credentials = json.load(f)

    def get_user_key(self):
        return self.credentials[self.DOW_JONES_CONFIG_KEY]['user_key']

    def get_google_cloud_project_name(self):
        return self.credentials[self.DOW_JONES_CONFIG_KEY]['project_name']

    def get_topic(self):
        return self.credentials[self.DOW_JONES_CONFIG_KEY]['topic']