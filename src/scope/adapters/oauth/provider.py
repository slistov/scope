import abc
from ...domain import security
from typing import List


class OAuthProvider:
    def __init__(
        self,
        name: str,
        code_url,
        scopes: List[str],
        token_url,
        state=None
    ) -> None:
        self.name = name
        self.code_url = code_url
        self.scopes = scopes
        self.token_url = token_url
        self.state = state if state else self.generate_state()

    def generate_state(self):
        return security.generate_secret()

    def get_auth_code_redirect_uri(self):
        return self._get_auth_code_redirect_uri()

    def get_state(self):
        return self.state

    def get_scopes_str(self):
        return ' '.join(self.scopes)

    @abc.abstractmethod
    def _get_auth_code_redirect_uri(self):
        raise NotImplementedError
