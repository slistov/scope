from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter

from ...service_layer import unit_of_work
from ...service_layer import messagebus
from ...service_layer.messagebus import commands

oauth_router = APIRouter(
    prefix="/oauth",
    tags=["OAuth 2.0"],
    responses={404: {"description": "Not found"}},
)


@oauth_router.get("/redirect")
async def api_get_oauth_redirect_uri(provider_name):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    cmd = commands.CreateAuthorization("origin")
    [state_code] = messagebus.handle(cmd, uow)
    return get_oauth_uri(state_code)


@oauth_router.get("/callback")
async def api_oauth_callback(state, code):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    actions_todo = [
        commands.ProcessGrantRecieved(
            params.state,
            "authorization_code",
            params.code
        ),
        commands.RequestToken(params.code)
    ]
    for msg in actions_todo:
        messagebus.handle(msg, uow)
    return 200
