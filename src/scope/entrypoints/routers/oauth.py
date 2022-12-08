from fastapi.routing import APIRouter
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException

from ...service_layer.services import services

from .google import google_router
from ...service_layer import services

oauth_router = APIRouter(
    prefix="/oauth",
    tags=["OAuth 2.0"],
    responses={404: {"description": "Not found"}},
)
oauth_router.include_router(google_router)


# TODO move to config
oauth_providers = {
    'google': services.OAuthGoogleRequester
}


@oauth_router.get("/redirect")
async def api_get_oauth_redirect_uri(provider_name) -> RedirectResponse:
    try:
        provider = oauth_providers[provider_name]()
    except KeyError:
        return HTTPException(
            400,
            {
                'error': 'provider_error',
                'description': 'Invalid provider name specified'
            }
        )
    return RedirectResponse(provider.get_auth_code_redirect_uri())
