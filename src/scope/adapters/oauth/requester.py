import abc
from .provider import OAuthProvider
from urllib.parse import urlencode

# from typing import Dict, List


class OAuthRequester:
    def __init__(self, provider) -> None:
        self.provider = provider

    def get_auth_code_redirect_uri(self):
        return self.provider.get_auth_code_redirect_uri()

    def exchange_code_for_token(self):
        return self._exchange_code_for_token()

    def validate_token(self, token: str):
        return self._validate_token(token)

    def get_access_token_validated(self):
        return self._get_access_token_validated()

    @abc.abstractmethod
    def _exchange_code_for_token(self):
        return NotImplementedError

    @abc.abstractmethod
    def _validate_token(self, token):
        return NotImplementedError

    @abc.abstractmethod
    def _get_access_token_validated(self):
        return NotImplementedError
