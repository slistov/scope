from fastapi import Depends
from fastapi.routing import APIRouter
from ....service_layer import schemas


google_router = APIRouter(
    prefix="/google",
    tags=["OAuth 2.0"],
    responses={404: {"description": "Not found"}},

)


@google_router.get("/")
async def api_google_callback(
    params: schemas.OAuthGoogleCallback = Depends(),
):
    pass
    return 200
