from datetime import datetime
from urllib.parse import urlencode

import pandas as pd
import requests

from .Creds import KeyringApiCredentials


class Api:
    """
    Interact with the GoDaddy API.  To acquire an API key and secret, log into GoDaddy 
    and navigate to: 
    https://developer.godaddy.com/keys.  

    There is a testing URL for the API at: 
    https://api.ote-godaddy.com  
    It only returns "Unauthorized" errors as of June 2023 even with valid OTE 
    credentials, it is included in this class in case the authentication error is fixed 
    in the future.
    """
    def __init__(self, creds: KeyringApiCredentials, testing: bool = False) -> None:
        if testing is True:
            self.BASE_URL = 'https://api.ote-godaddy.com'
        else:
            self.BASE_URL = 'https://api.godaddy.com'
        self.MARKET = 'en-US'
        self.creds = creds
        self.__sso_key = f'sso-key {self.creds.api_key}:{self.creds.api_secret}'
        self.__headers = {
            'accept': 'application/json',
            'X-Market-Id': self.MARKET,
            'Authorization': self.__sso_key
        }

    def __repr__(self) -> str:
        return f"{self.creds.name = }"

    def __str__(self) -> str:
        return f"{self.creds.name = }"

    @staticmethod
    def get_report_name(subject: str) -> str:
        now = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
        return f"{now} GoDaddy {subject} Report.xlsx"

    def get_subscriptions(self, limit: int = 250) -> requests.Response:
        """
        The GoDaddy subscriptions endpoint provides a list of all the current
        subscriptions, expiration date, label, and status.
        """
        version = 'v1'
        fields = {
            'offset': '0',
            'limit': str(limit),
            'sort': 'expiresAt'
        }
        url = f'{self.BASE_URL}/{version}/subscriptions?{urlencode(fields)}'
        return requests.get(url, headers=self.__headers)

    def get_orders(self, limit: int = 500) -> requests.Response:
        """
        The GoDaddy orders endpoint provides a list of past orders.
        """
        version = 'v1'
        fields = {
            'offset': '0',
            'limit': str(limit),
            'sort': '-createdAt'
        }
        url = f'{self.BASE_URL}/{version}/orders?{urlencode(fields)}'
        return requests.get(url, headers=self.__headers)
    
    def response_to_dataframe(self, response: requests.Response) -> pd.DataFrame:
        """Skip the parent key (informational only) and return a flattened dataframe."""
        return pd.json_normalize(next(iter(response.json().values())))
    
    def create_report(self, api_call: str, subject: str) -> None:
        """Save a spreadsheet of the flattened data from the API call."""
        api_call_method = getattr(self, api_call)
        response = api_call_method()
        response.raise_for_status()
        df = self.response_to_dataframe(response)
        report_name = self.get_report_name(subject)
        df.to_excel(report_name, index=False)
        print(f'Created report: "{report_name}"')