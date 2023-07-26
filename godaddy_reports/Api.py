from datetime import datetime
from urllib.parse import urlencode
from abc import ABC, abstractmethod

import pandas as pd
import requests

from .Creds import KeyringApiCredentials


class Call(ABC):
    
    def __init__(self,
                 creds: KeyringApiCredentials,
                 output: str,
                 test: bool = False) -> None:
        if test is True:
            self.BASE_URL = 'https://api.ote-godaddy.com'
        else:
            self.BASE_URL = 'https://api.godaddy.com'
        self.MARKET = 'en-US'
        self.creds = creds
        self.output = output
        self.url = None
        self.__sso_key = f'sso-key {self.creds.api_key}:{self.creds.api_secret}'
        self.__headers = {
            'accept': 'application/json',
            'X-Market-Id': self.MARKET,
            'Authorization': self.__sso_key
        }

    @property
    @abstractmethod
    def subject(self) -> str:
        pass

    @abstractmethod
    def build_request(self) -> str:
        pass

    @property
    def report_name(self) -> str:
        now = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
        return f"{now} GoDaddy Report - {self.subject}.xlsx"

    def send_request(self, url: str) -> requests.Response:
        return requests.get(url, headers=self.__headers)

    def response_to_dataframe(self, response: requests.Response) -> pd.DataFrame:
        """Skip the parent key (informational only) and return a flattened dataframe."""
        return pd.json_normalize(next(iter(response.json().values())))
    
    def create_report(self) -> None:
        """Save a spreadsheet of the flattened data from the API call."""
        request = self.build_request()
        response = self.send_request(request)
        response.raise_for_status()
        df = self.response_to_dataframe(response)
        if self.output == 'xlsx':
            df.to_excel(self.report_name, index=False)
        elif self.output == 'csv':
            df.to_csv(self.report_name, index=False)
        else:
            raise ValueError
        print(f'Created report: "{self.report_name}"')


class Subscriptions(Call):
    """
    The GoDaddy subscriptions endpoint provides a list of all the current
    subscriptions, expiration date, label, and status.
    """
    @property
    def subject(self) -> str:
        return "Subscriptions"

    def build_request(self,
                      offset: int = 0,
                      limit: int = 250,
                      sort: str = 'expiresAt') -> str:
        version = 'v1'
        fields = {
            'offset': str(offset),
            'limit': str(limit),
            'sort': sort
        }
        return f'{self.BASE_URL}/{version}/subscriptions?{urlencode(fields)}'
    
class Orders(Call):
    """
    The GoDaddy orders endpoint provides a list of past orders.
    """
    @property
    def subject(self) -> str:
        return "Orders"

    def build_request(self,
                      offset: int = 0,
                      limit: int = 500,
                      sort: str = '-createdAt') -> str:
        version = 'v1'
        fields = {
            'offset': str(offset),
            'limit': str(limit),
            'sort': sort
        }
        return f'{self.BASE_URL}/{version}/orders?{urlencode(fields)}'
