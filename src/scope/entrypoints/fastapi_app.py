from fastapi import FastAPI, Response, status, Body
from fastapi.encoders import jsonable_encoder

from .routers import user_router
import json
from elasticsearch import Elasticsearch
import scope.entrypoints.schemas as schemas


app = FastAPI()

app.include_router(user_router)

@app.get('/')
def api_get_root():
    return Response(status_code=status.HTTP_200_OK)

@app.post("/indexes")
def api_indexes_add(doc: schemas.Quote = Body()):
    doc_json = jsonable_encoder(doc)
    es = Elasticsearch(
        "https://192.168.99.100:9200", 
        ca_certs="http_ca.crt",
        basic_auth=("elastic", '+*CZTWqSJpbACQnm1MRY')
    )
    return es.index(index="index-quotes", id='1', document=doc_json)