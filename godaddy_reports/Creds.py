import os
from dataclasses import dataclass
from getpass import getpass

import keyring


@dataclass
class KeyringApiCredentials:
    """GoDaddy API credentials and information about the keyring storing them."""
    name: str # Name of the credentials in the keyring.
    api_key: str # GoDaddy API key, stored as "username" in keyring.
    api_secret: str # GoDaddy API secret, stored as "password" in keyring.
    key_ring: str # Name of the keyring depending on operating system

def get_keyring_creds(creds_name: str, creds_api_key: str) -> KeyringApiCredentials:
    """Get GoDaddy API credentials from the keyring."""
    credentials = keyring.get_credential(creds_name, creds_api_key)
    if os.name == 'nt':
        key_ring = 'Credentials Manager'
    else:
        key_ring = 'Keyring'
    try:
        return KeyringApiCredentials(
            name=creds_name,
            api_key=creds_api_key,
            api_secret=credentials.password,
            key_ring=key_ring)
    except AttributeError:
        return KeyringApiCredentials(
            name=creds_name,
            api_key=creds_api_key,
            api_secret=None,
            key_ring=key_ring)

def set_keyring_creds(creds_name: str, creds_api_key: str) -> KeyringApiCredentials:
    """Set GoDaddy API credentials values in the keyring."""
    api_secret = getpass('Enter GoDaddy API Secret: ')
    keyring.set_password(creds_name, creds_api_key, api_secret)
    if os.name == 'nt':
        key_ring = 'Credentials Manager'
    else:
        key_ring = 'Keyring'
    print(f'Stored GoDaddy API secret in {key_ring} as "{creds_name}"')
    return KeyringApiCredentials(
            name=creds_name,
            api_key=creds_api_key,
            api_secret=api_secret,
            key_ring=key_ring)