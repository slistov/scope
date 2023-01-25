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
    cmd = commands.CreateAuthorization("origin", provider_name=provider_name)
    [state_code] = await messagebus.handle(cmd, uow)
    return await messagebus.get_oauth_uri(state_code)


@oauth_router.get("/callback")
async def api_oauth_callback(state, code):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    actions_todo = [
        commands.ProcessGrantRecieved(
            state,
            "authorization_code",
            code
        ),
        commands.RequestToken(grant_code=code)
    ]
    for msg in actions_todo:
        results = await messagebus.handle(msg, uow)
    [code, access_token] = results
    return {"access_token": access_token}
