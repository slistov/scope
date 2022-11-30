from fastapi import Query
from fastapi.routing import APIRouter
from ...service_layer.services import get_email_check_code


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
    return get_email_check_code(email)
