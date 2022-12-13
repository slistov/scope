from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from ..domain import model
from ..adapters.repository import (
    SQLAlchemyAccountsRepository,
    SQLAlchemyEmailsRepository
)
from .emails import send_confirm_email

from ..adapters.oauth.requester import OAuthRequester
from ..adapters.oauth.provider import OAuthProvider


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


def get_oauth_redirect(provider: OAuthProvider) -> str:
    requester = OAuthRequester(provider)
    return requester.get_auth_code_redirect_uri()


async def exchange_code_for_token(code, provider: OAuthProvider) -> str:
    requester = OAuthRequester(provider)
    token = await requester.exchange_code_for_token(code)
    user = await requester.parse_id_token(token)
    return 200
