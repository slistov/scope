import abc

from typing import Dict, List
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from ..domain import model
from ..adapters.repository import (
    SQLAlchemyAccountsRepository,
    SQLAlchemyEmailsRepository
)
from .emails import send_confirm_email


class OAuthRequester():
    code_url = ''
    scopes = []
    token_url = ''

    def __init__(self) -> None:
        self.scopes: Dict[str: List] = {}
        self.code = ''
        self.access_token = ''
        self.refresh_token = ''

    def get_auth_code_redirect_uri(self):
        return self._get_auth_code_redirect_uri()

    def exchange_code_for_token(self):
        return self._exchange_code_for_token()

    def validate_token(self, token: str):
        return self._validate_token(token)

    def get_access_token_validated(self):
        return self._get_access_token_validated()

    @abc.abstractmethod
    def _get_auth_code_redirect_uri():
        return NotImplementedError

    @abc.abstractmethod
    def _exchange_code_for_token(self):
        return NotImplementedError

    @abc.abstractmethod
    def _validate_token(self, token):
        return NotImplementedError

    @abc.abstractmethod
    def _get_access_token_validated(self):
        return NotImplementedError


class OAuthGoogleRequester(OAuthRequester):
    code_url = 'https://accounts.google.com/o/oauth2/v2/auth'
    scopes = ['https://www.googleapis.com/auth/userinfo.email']
    token_url = 'https://oauth2.googleapis.com/token'

    def _get_auth_code_redirect_uri(self):
        pass

    def _exchange_code_for_token(self):
        pass


async def create_account(email, password, repo=SQLAlchemyAccountsRepository()):
    with repo:
        e = model.Email(email, is_main=True)
        await send_confirm_email(e.email, e.check_code)
        a = model.Account(email=e, password=password)
        repo.add(a)
        repo.commit()
        return {"check_code": e.get_check_code()}


def confirm_email(email, code, repo=SQLAlchemyEmailsRepository()):
    with repo:
        e = repo.get_by_email(email)
        # TODO if checks must be explicitly
        if e.confirm(code):
            repo.commit()
            return jsonable_encoder(e)
        else:
            return HTTPException(
                400,
                {
                    'error': "Couldn't confirm email"
                }
            )
