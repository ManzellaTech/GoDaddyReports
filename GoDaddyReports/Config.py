import json
import os
import tempfile
from getpass import getpass


class Config:
    def __init__(self):
        self.config_path = os.path.join(tempfile.gettempdir(), 'gd_config.json')

        config = None
        if os.path.isfile(self.config_path):
            with open(self.config_path, 'r') as infile:
                config = json.load(infile)
                if len(config) == 0:
                    config = None
        if isinstance(config, dict):
            self.creds_name = config['creds_name']
            self.api_key = config['api_key']
        else:
            self.creds_name = None
            self.api_key = None

    def set_config(self, creds_name: str) -> None:
        api_key = getpass('Enter GoDaddy API Key: ')
        if len(creds_name) > 0 and isinstance(creds_name, str) and len(api_key) > 0:
            config = {
                'creds_name': creds_name,
                'api_key': api_key,
            }
            with open(self.config_path, 'w') as outfile:
                json.dump(config, outfile)
            print('Set config file containing the credentials name and API key in '
                 f'{self.config_path}')
            self.creds_name = creds_name
            self.api_key = api_key
        else:
            raise ValueError('Credentials name and GoDaddy API key both must contain '
                             'at least one character and be strings.')
