from fastapi import Depends
from fastapi.requests import Request
from fastapi.routing import APIRouter

from ....adapters import oauth
from ....service_layer import schemas, services

google_router = APIRouter(
    prefix="/google",
    tags=["OAuth 2.0"],
    responses={404: {"description": "Not found"}},

)


@google_router.get("/")
async def api_google_callback(
    request: Request,
    params: schemas.OAuthGoogleCallback = Depends(),
):
    provider = oauth.OAuthGoogleProvider()
    services.exchange_code_for_token(params.code, provider)
    user_email = await provider.get_user_email()
    return user_email
