from fastapi import FastAPI, Response, status

from .routers import account_router
from ..adapters import orm

app = FastAPI()
orm.start_mappers()

app.include_router(account_router)


@app.get('/')
def api_get_root():
    return Response(status_code=status.HTTP_200_OK)
