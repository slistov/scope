from typing import Dict, List
from fastapi import HTTPException


class OauthRequester():
    def __init__(self) -> None:
        self.scopes: Dict[str: List] = {}

    def validate_token(self, token: str):
        if not token == 'test_token':
            raise HTTPException(status_code=400, detail={'error': 'not test_token'})
        scopes = "read write".split()
        self.scopes.update({token: scopes})
        return True
