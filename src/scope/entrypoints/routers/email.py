from fastapi import Query
from fastapi.routing import APIRouter
from ...service_layer.services import create_account


email_router = APIRouter(
    prefix="/emails",
    tags=["emails"],
    responses={404: {"description": "Not found"}},
)


@email_router.post(
    path="/",
    description="Get confirmation code for email provided"
)
def api_get_confirmation_code(
    email: str = Query(..., description="Email to register")
):
    return create_account(email)
