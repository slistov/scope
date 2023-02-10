from fastapi import FastAPI, Response, status
from oauth_client_lib import oauth_router
# from oauth_client_lib.entrypoints.routers.oauth import oauth_router
from starlette.middleware.sessions import SessionMiddleware

from ..adapters import orm
from ..domain.security import generate_client_secret
from .routers import account_router

app = FastAPI()
orm.start_mappers()

app.include_router(account_router, prefix='/api')
app.include_router(oauth_router, prefix='/api')

app.add_middleware(SessionMiddleware, secret_key=generate_client_secret())


@app.get('/')
def api_get_root():
    return Response(status_code=status.HTTP_200_OK)
