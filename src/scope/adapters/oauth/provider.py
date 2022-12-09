import abc
from typing import List


class OAuthProvider:
    name = ''
    code_url = ''
    scopes: List[str] = []
    token_url = ''

    def get_auth_code_redirect_uri(self):
        return self._get_auth_code_redirect_uri()

    @abc.abstractmethod
    def _get_auth_code_redirect_uri(self):
        raise NotImplementedError
