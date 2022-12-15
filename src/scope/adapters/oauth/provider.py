import abc
from ...domain import security
from typing import List
from ... import config
import aiohttp
import base64


class OAuthProvider:
    def __init__(
        self,
        name: str,
        code_url,
        scopes: List[str],
        token_url,
        state=None,
        public_keys_url='',
        public_keys: List[dict] = []
    ) -> None:
        self.name = name
        self.code_url = code_url
        self.scopes = scopes
        self.token_url = token_url
        self.state = state if state else self.__generate_state()
        self.public_keys_url = public_keys_url
        self.public_keys = public_keys

    def get_authorize_uri(self):
        return self._get_authorize_uri()

    @abc.abstractmethod
    def _get_authorize_uri(self):
        raise NotImplementedError

    def get_user_email(self):
        parsed_id_token = self._parse_id_token()
        return parsed_id_token['email']

    def _get_redirect_uri(self):
        return f'{config.get_oauth_redirect_uri()}/{self.name}'

    def _get_scopes_str(self):
        assert self.scopes
        return ' '.join(self.scopes)

    async def _request_public_keys(self):
        assert self.public_keys_url
        keys = await async_get_request(self.public_keys_url)
        return keys

    def _get_public_key(self, kid):
        if not self.public_keys or self.public_keys == []:
            self.public_keys = self._request_public_keys()
        for key in self.public_keys:
            if key.pop("kid", None) == kid:
                return key
        return None

    def __generate_state(self):
        return security.generate_secret()

    def _parse_id_token(self):
        id_token = self.credentials.id_token
        jwt_header = id_token.split('.')[0]
        header = base64.b64decode(jwt_header)

        kid = header['kid']
        alg = header['alg']
        try:
            token_data = security.decode_jwt(
                id_token,
                key=self._get_public_key(kid),
                algorithm=alg,
                verify_signature=True
            )
        except Exception as e:
            return None
        return token_data


async def async_get_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            result = await resp.json()
            return result
