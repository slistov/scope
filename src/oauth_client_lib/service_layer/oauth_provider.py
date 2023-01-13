from urllib.parse import urlencode

import aiohttp
import json
import requests

from ..config import get_oauth_callback_URL
from ..domain import commands, model
from ..service_layer import messagebus, unit_of_work
from . import exceptions
from .. import config
from ..adapters import orm

orm.start_mappers()


class OAuthProvider:
    def __init__(
        self,
        provider_name,
        client_id='',
        client_secret='',
        code_url=None,
        token_url=None,
        scopes=[],
        public_keys_url='',
    ):
        (
            _scopes,
            _code_url,
            _token_url,
            _public_keys_url
        ) = self.__class__._get_provider_params(provider_name)

        self.provider_name = provider_name
        self.code_url = code_url if code_url else _code_url
        self.token_url = token_url if token_url else _token_url
        self.scopes = scopes if scopes else _scopes
        self.public_keys_url = public_keys_url if public_keys_url else _public_keys_url

        (
            self.client_id,
            self.client_secret
        ) = self.__class__._get_oauth_secrets(provider_name)

    @classmethod
    def by_state(cls, state):
        """OAuthProvider constructor by state"""
        s = model.State(state)
        a = model.Authorization(state=s)
        return cls(a.provider_name)

    @staticmethod
    def _get_oauth_secrets(provider_name):
        with open(f'client_secret_{provider_name}.json') as f:
            secrets = json.load(f)["web"]
            return secrets["client_id"], secrets["client_secret"]

    async def get_authorize_uri(self, uow=None):
        assert self.code_url, "code_url is not provided"
        uow = unit_of_work.SqlAlchemyUnitOfWork() if not uow else uow
        cmd = commands.CreateAuthorization("origin")
        [state_code] = await messagebus.handle(cmd, uow)
        return self._get_oauth_uri(state_code)

    async def request_token(self, code) -> requests.Response:
        data = self._get_tokenRequest_data(grant=grant)
        self.response = await self._post(
            url=self.token_url,
            data=data
        )
        return self.response

    @staticmethod
    def _get_provider_params(name):
        scopes, urls = config.get_oauth_params(name)
        return scopes, urls['code'], urls['token'], urls['public_keys']

    def _get_oauth_uri(self, state_code):
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": get_oauth_callback_URL(),
            "scope": ' '.join(self.scopes),
            "state": state_code
        }
        uri = f"{self.code_url}?{urlencode(params,)}"
        return uri

    def _get_tokenRequest_data(self, grant):
        if grant.grant_type == "authorization_code":
            data = {
                "code": grant.code,
                "redirect_uri": get_oauth_callback_URL()
            }
        elif grant.grant_type == "refresh_token":
            data = {"refresh_token": grant.code}
        else:
            raise exceptions.InvalidGrant(f"Unknown grant type {grant.grant_type} while requesting token")

        assert self.client_id
        assert self.client_secret
        data.update({
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": grant.grant_type
        })
        return data

    async def _post(self, url, data):
        return await post_async(
            url=url,
            data=data
        )

    def get_token(self) -> model.Token:
        return model.Token(self._get_token_str())

    def get_grant(self) -> model.Grant:
        return model.Grant("refresh_token", self._get_grant_code())

    def _get_token_str(self):
        return self.response.json().get("access_token", None)
        # return self.response

    def _get_grant_code(self):
        return self.response.json().get("refresh_token", None)
        # return self.response.get("refresh_token", None)


async def post_async(url, data):
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            url=url,
            data=data
        )
        return response.json()
