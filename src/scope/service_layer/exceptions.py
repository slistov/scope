from fastapi.exceptions import HTTPException


class OAuthException(HTTPException):
    pass


class WrongStateOAuthException(OAuthException):
    pass
