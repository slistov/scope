from fastapi import APIRouter, Depends, Query
from ..dependencies import token_scopes_read_write
from ...service_layer.services import get_email_check_code



account_router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    dependencies=[Depends(token_scopes_read_write)],
    responses={404: {"description": "Not found"}}
)


@account_router.post(
    path="/",
    description="Get confirmation code for email provided"
)
def api_get_confirmation_code(
    email: str = Query(..., description="Email to register")
):
    return get_email_check_code(email)


@account_router.get("/")
def api_users_get():
    return {"message": "ok"}
