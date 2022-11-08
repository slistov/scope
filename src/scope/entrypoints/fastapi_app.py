from elasticsearch import AsyncElasticsearch
from fastapi import Body, Depends, FastAPI, Response, status
from fastapi.encoders import jsonable_encoder

import scope.entrypoints.schemas as schemas

from .. import config
from .routers import user_router

app = FastAPI()

app.include_router(user_router)


@app.get('/')
def api_get_root():
    return Response(status_code=status.HTTP_200_OK)


@app.put("/indexes")
async def api_indexes_add():
    
    user, password = config.get_es_user_credentials()
    es = AsyncElasticsearch(
        config.get_es_uri(), 
        basic_auth=(user, password),
        verify_certs=False
    )
    index = await es.indices.create(index="quotes")
    return 200


@app.post("/indexes")
async def api_indexes_add_doc(doc: schemas.Quote = Body()):
    es = AsyncElasticsearch(
        "https://192.168.99.100:9200", 
        basic_auth=("elastic", "P18sc1v5CxZgqh9dhqGC"),
        verify_certs=False
    )
    return await es.index(index="index-quotes", id='1', document=doc.json())


@app.get("/indexes/{index}/{id}")
async def api_indexes_get_by_id(index, id):
    es = AsyncElasticsearch(
        "https://192.168.99.100:9200", 
        basic_auth=("elastic", "P18sc1v5CxZgqh9dhqGC"),
        verify_certs=False
    )
    return await es.get(index=index, id=id)


@app.get("/indexes")
async def api_indexes_get_by_pattern(query_params: schemas.QuoteQueryParams = Depends()):
    es = AsyncElasticsearch(
        "https://192.168.99.100:9200", 
        basic_auth=("elastic", "P18sc1v5CxZgqh9dhqGC"),
        verify_certs=False
    )
    query_params_json = jsonable_encoder(query_params)
    match_list = [
        {"match": {field_name: field_value}} for field_name, field_value in query_params_json.items()
    ]
    resp = await es.search(
        index="index-quotes", 
        query={
            "bool": {
                "must": match_list
            }
        }
    )
    return resp
