from fastapi import APIRouter, Depends, Query
from ..dependencies import token_scopes_read_write
from ...service_layer.services import create_account


account_router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    responses={404: {"description": "Not found"}}
)


@account_router.post(
    path="/",
    description="Create account, using contact data. Confirmation code will be sent"
)
async def api_create_account(
    email: str = Query(..., description="Email to register"),
    password: str = Query(..., description="User password")
):
    return await create_account(email, password)


@account_router.get("/")
def api_users_get():
    return {"message": "ok"}


# dependencies=[Depends(token_scopes_read_write)],