from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from oauth_client_lib import OAuthProvider

from ..adapters.repository import (SQLAlchemyAccountsRepository,
                                   SQLAlchemyEmailsRepository)
from ..domain import model
from .emails import send_confirm_email
from . import exceptions
from .. import config


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


async def get_oauth_authorize_uri(
    provider: OAuthProvider = None,
    provider_name: str = ''
) -> str:
    if not provider:
        assert provider_name, "provider_name is not provided. Ex.: 'google'"
        client_id, _ = config.get_oauth_secrets(provider_name)
        try:
            provider = OAuthProvider(provider_name, client_id=client_id)
        except KeyError:
            return HTTPException(
                400,
                {
                    'error': 'provider_error',
                    'description': 'Invalid provider name specified'
                }
            )
    return await provider.get_authorize_uri()


def exchange_code_for_token(code, provider: OAuthProvider) -> str:
    requester = OAuthRequester(provider)
    token = requester.exchange_code_for_token(code)
    return token


async def get_token_for_auth_code(state, code):
    try:
        provider = OAuthProvider(state=state)
    except StateInvalid as e:
        raise
    except StateExpired as e:
        raise
    except AuthorizationInvalid as e:
        raise
    token = await provider.get_token(code)
    return token
