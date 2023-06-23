from GoDaddyReports.Creds import CredentialsFactory
from GoDaddyReports.Api import Api
from GoDaddyReports.Config import Config

"""
Generate spreadsheets of reports pulled from GoDaddy's API.
The purpose is to provide data about GoDaddy's current subscriptions, orders,
etcetera to IT and Accounts Payable departments. 
"""

CREDENTIALS_NAME = 'GoDaddy API'
        
def main(creds_name: str) -> None:
    cfg = Config()
    if cfg.creds_name is None or cfg.api_key is None:
        cfg.set_config(creds_name=CREDENTIALS_NAME) 
    creds = CredentialsFactory.get_gd_creds(creds_name=creds_name,
                                            creds_api_key=cfg.api_key)
    if creds.api_secret is None:
        creds = CredentialsFactory.set_gd_creds(creds_name=creds_name,
                                                creds_api_key=cfg.api_key)
    api = Api(creds)
    api.create_report(api_call='get_subscriptions', subject='Subscriptions')
    api.create_report(api_call='get_orders', subject='Orders')

if __name__ == '__main__':
    main(creds_name=CREDENTIALS_NAME)