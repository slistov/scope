from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from ..adapters.oauth.provider import OAuthProvider
from ..adapters.oauth.requester import OAuthRequester
from ..adapters.repository import (SQLAlchemyAccountsRepository,
                                   SQLAlchemyEmailsRepository)
from ..domain import model
from .emails import send_confirm_email
from . import exceptions

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


def get_oauth_authorize_uri(provider: OAuthProvider) -> str:
    requester = OAuthRequester(provider)
    return requester.get_authorize_uri()


def exchange_code_for_token(code, provider: OAuthProvider) -> str:
    requester = OAuthRequester(provider)
    token = requester.exchange_code_for_token(code)
    return token


def validate_code_response(code, state, db_adapter: AbstractRepository):
    authorization = db_adapter.get_authorization(state)
    if not authorization:
        # TODO
        pass
    
    authorization.code = code
    return {'message': 'authorization code accepted'}