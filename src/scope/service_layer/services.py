from typing import Dict, List
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from ..domain import model
from ..adapters.repository import SQLAlchemyAccountsRepository, SQLAlchemyEmailsRepository
from .emails import send_confirm_email
from . import schemas


class OauthRequester():
    def __init__(self) -> None:
        self.scopes: Dict[str: List] = {}

    def validate_token(self, token: str):
        if not token == 'test_token':
            raise HTTPException(
                status_code=400,
                detail={'error': 'not test_token'}
            )
        scopes = "read write".split()
        self.scopes.update({token: scopes})
        return True


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
