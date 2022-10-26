from fastapi import APIRouter, Depends
from ..dependencies import token_scopes_read_write



user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(token_scopes_read_write)],
    responses={404: {"description": "Not found"}},
)


@user_router.get("/")
def api_users_get():
    return {"message": "ok"}