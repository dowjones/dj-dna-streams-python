import os
import json


class Config():

    DOW_JONES_APPLICATION_CREDENTIALS = 'DOW_JONES_APPLICATION_CREDENTIALS'
    DOW_JONES_CONFIG_KEY = 'dj_dna_streaming'

    def __init__(self):

        needs_credentials = self.DOW_JONES_APPLICATION_CREDENTIALS not in os.environ

        if needs_credentials:
            raise Exception('Encountered problem reading required environmental variable \'{0}\'.'
                            .format(self.DOW_JONES_APPLICATION_CREDENTIALS) +
                            'Did you set the environment variable \'{0}\' to the path of your Dow Jones provided security file?'
                            .format(self.DOW_JONES_APPLICATION_CREDENTIALS))

        self.credentials_path = os.environ[self.DOW_JONES_APPLICATION_CREDENTIALS]

        if not os.path.isfile(self.credentials_path):
            raise Exception('Encountered problem finding file at path \'{}\'. Does it exist?'.format(self.credentials_path))

        if not os.access(self.credentials_path, os.R_OK):
            raise Exception('Encountered permission problem reading file from path \'{}\'.'.format(self.credentials_path))

        with open(self.credentials_path, 'r') as f:
            self.credentials = json.load(f)

    def get_user_key(self):
        return self.credentials[self.DOW_JONES_CONFIG_KEY]['user_key']

    def get_google_cloud_project_name(self):
        project_name = 'djsyndicationhub-prod'
        if 'project_name' in self.credentials[self.DOW_JONES_CONFIG_KEY]:
            tmp_project_name = self.credentials[self.DOW_JONES_CONFIG_KEY]['project_name']
            if tmp_project_name and len(tmp_project_name.strip()) > 0:
                project_name = tmp_project_name.strip()

        return project_name

    def get_topic(self):
        return self.credentials[self.DOW_JONES_CONFIG_KEY]['topic']
