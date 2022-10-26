from fastapi import FastAPI, Response, status
from .routers import user_router

app = FastAPI()

app.include_router(user_router)

@app.get('/')
def api_get_root():
    return Response(status_code=status.HTTP_200_OK)