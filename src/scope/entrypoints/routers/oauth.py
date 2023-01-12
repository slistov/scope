from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter


from .google import google_router

from ...service_layer import services

oauth_router = APIRouter(
    prefix="/oauth",
    tags=["OAuth 2.0"],
    responses={404: {"description": "Not found"}},
)

# TODO do not always init, only if google specified
oauth_router.include_router(google_router)


# TODO move to config
# oauth_providers = {
#     'google': OAuthGoogleProvider
# }


# @oauth_router.get("/redirect")
# async def api_get_oauth_redirect_uri(provider_name):
#     try:
#         provider = oauth_providers[provider_name]()
#     except KeyError:
#         return HTTPException(
#             400,
#             {
#                 'error': 'provider_error',
#                 'description': 'Invalid provider name specified'
#             }
#         )
#     return RedirectResponse(provider.get_authorize_uri())

@oauth_router.get("/redirect")
async def api_get_oauth_redirect_uri(provider_name):
    uri = await services.get_oauth_authorize_uri(provider_name=provider_name)
    return RedirectResponse(uri)

@oauth_router.get("/callback")
async def api_oauth_callback(state, code):
    token = await services.get_token_for_auth_code(state, code)
    return token