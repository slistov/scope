import abc
from typing import List

import aiohttp
from jose import jws, jwt

from ... import config
from ...domain import security


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

    async def get_user_email(self):
        parsed_id_token = await self._parse_id_token()
        return parsed_id_token['email']

    def _get_redirect_uri(self):
        return f'{config.get_oauth_redirect_uri()}/{self.name}'

    def _get_scopes_str(self):
        assert self.scopes
        return ' '.join(self.scopes)

    async def _request_public_keys(self):
        assert self.public_keys_url
        result = await async_get_request(self.public_keys_url)
        return result['keys']

    async def _get_public_key(self, kid):
        if not self.public_keys or self.public_keys == []:
            self.public_keys = await self._request_public_keys()
        for key in self.public_keys:
            if key.pop("kid", None) == kid:
                return key
        return None

    def __generate_state(self):
        return security.generate_secret()

    async def _parse_id_token(self):
        id_token = self.credentials.id_token

        kid = jws.get_unverified_header(id_token)['kid']
        alg = jws.get_unverified_header(id_token)['alg']
        try:
            token_data = jwt.decode(
                id_token,
                key=await self._get_public_key(kid),
                algorithms=[alg],
                audience=self.flow.credentials.client_id
            )
        except Exception as e:
            return None
        return token_data


async def async_get_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            result = await resp.json()
            return result
