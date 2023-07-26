from godaddy_reports import Creds, Subscriptions, Orders, Config
from argparse import ArgumentParser

"""
Generate spreadsheets of reports pulled from GoDaddy's API.
The purpose is to provide data about GoDaddy's current subscriptions, orders,
etcetera to IT and Accounts Payable departments. 
"""

parser = ArgumentParser(description='Options for script.')
parser.add_argument('-t', '--test',
                    action='store_true',
                    dest='test',
                    help='Test run of the script.  No changes will be made.')
parser.add_argument('-o', '--output',
                    choices=['xlsx', 'csv'],
                    default='xlsx',
                    dest='output',
                    help='File type that should be output.')
parser.add_argument('-c', '--creds',
                    choices=['input', 'keyring', 'env_vars'],
                    default='keyring',
                    dest='creds',
                    help='Decide how to accept and store credentials. '
                         '"input" will require credentials to be input. '
                         '"keyring" will store credentials in the keyring the read '
                         'them from the keyring. '
                         '"env_vars"  will store credentials as environment variables '
                         'and read them from environment variables.')
args = parser.parse_args()

CREDENTIALS_NAME = 'GoDaddy API'
        
def main(creds_name: str) -> None:
    if args.creds == 'keyring':
        cfg = Config()
        if cfg.creds_name is None or cfg.api_key is None:
            cfg.set_config(creds_name=CREDENTIALS_NAME) 
        creds = Creds.get_keyring_creds(creds_name=creds_name,
                                        creds_api_key=cfg.api_key)
        if creds.api_secret is None:
            creds = Creds.set_keyring_creds(creds_name=creds_name,
                                            creds_api_key=cfg.api_key)
    if args.test is False:
        Subscriptions(creds, args.output).create_report()
        Orders(creds, args.output).create_report()

if __name__ == '__main__':
    main(creds_name=CREDENTIALS_NAME)
