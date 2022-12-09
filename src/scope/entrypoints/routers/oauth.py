from fastapi.routing import APIRouter
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi.requests import Request

from .google import google_router
from ...adapters.oauth.google.google import OAuthGoogleProvider

oauth_router = APIRouter(
    prefix="/oauth",
    tags=["OAuth 2.0"],
    responses={404: {"description": "Not found"}},
)

# TODO do not always init, only if google specified
oauth_router.include_router(google_router)


# TODO move to config
oauth_providers = {
    'google': OAuthGoogleProvider
}


@oauth_router.get("/redirect")
async def api_get_oauth_redirect_uri(provider_name, request: Request):
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
    request.session["session_state"] = provider.state
    # return {'redirect_uri': provider.get_auth_code_redirect_uri()}
    return RedirectResponse(provider.get_auth_code_redirect_uri())
