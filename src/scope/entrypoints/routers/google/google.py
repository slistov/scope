from fastapi import Depends
from fastapi.requests import Request
from fastapi.routing import APIRouter
from ....service_layer import schemas

from ....adapters import 


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

    return user    
    
