from fastapi import FastAPI, Response, status
from starlette.middleware.sessions import SessionMiddleware

from .routers import account_router, oauth_router
from ..adapters import orm
from ..domain.security import generate_client_secret

app = FastAPI()
orm.start_mappers()

app.include_router(account_router, prefix='/api')
app.include_router(oauth_router, prefix='/api')

app.add_middleware(SessionMiddleware, secret_key=generate_client_secret())


@app.get('/')
def api_get_root():
    return Response(status_code=status.HTTP_200_OK)
