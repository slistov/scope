from fastapi import FastAPI, Response, status, Body

from .routers import user_router
import json
from elasticsearch import Elasticsearch
import scope.entrypoints.schemas as schemas

import ssl


app = FastAPI()

app.include_router(user_router)

@app.get('/')
def api_get_root():
    return Response(status_code=status.HTTP_200_OK)

@app.post("/indexes")
def api_indexes_add(doc: schemas.Quote = Body()):
    es = Elasticsearch(
        "https://192.168.99.100:9200", 
        ca_certs="http_ca.crt",
        basic_auth=("elastic", "P18sc1v5CxZgqh9dhqGC"),
        verify_certs=False
    )
    return es.index(index="index-quotes", id='1', document=doc.json())

@app.get("/indexes")
def api_indexes_get_by_id(index, id):
    es = Elasticsearch(
        "https://192.168.99.100:9200", 
        ca_certs="http_ca.crt",
        basic_auth=("elastic", "P18sc1v5CxZgqh9dhqGC"),
        verify_certs=False
    )
    return es.get(index=index, id=id)
