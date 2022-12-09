from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.requests import Request
from ....service_layer import schemas


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
    pass
    session_state = request.session.get("session_state", None)
    return 200
