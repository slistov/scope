from elasticsearch import AsyncElasticsearch
from fastapi import Body, Depends, FastAPI, Response, status
from fastapi.encoders import jsonable_encoder

import scope.entrypoints.schemas as schemas

from .. import config
from .routers import user_router
from ..service_layer import services
from . import dependencies 

app = FastAPI()

app.include_router(user_router)


@app.get('/')
def api_get_root():
    return Response(status_code=status.HTTP_200_OK)


@app.put("/indices/{index_name}")
async def api_indexes_add(index_name: str, docs_bulk = Body()):
    elastic_repo = dependencies.elastic_repo
    return await services.add_doc_to_index(elastic_repo, index_name, docs_bulk)


@app.get("/indices/{index_name}")
async def api_search_index_for_text(index_name, text):
    elastic_repo = dependencies.elastic_repo    
    return await services.search_index_for_text(elastic_repo, index_name, text)











# @app.post("/indices")
# async def api_indexes_add_doc(doc: schemas.Quote = Body()):
#     es = AsyncElasticsearch(
#         "https://192.168.99.100:9200", 
#         basic_auth=("elastic", "P18sc1v5CxZgqh9dhqGC"),
#         verify_certs=False
#     )
#     return await es.index(index="index-quotes", id='1', document=doc.json())


# @app.get("/indices/{index}/{id}")
# async def api_indexes_get_by_id(index, id):
#     es = AsyncElasticsearch(
#         "https://192.168.99.100:9200", 
#         basic_auth=("elastic", "P18sc1v5CxZgqh9dhqGC"),
#         verify_certs=False
#     )
#     return await es.get(index=index, id=id)


# @app.get("/indices")
# async def api_indexes_get_by_pattern(query_params: schemas.QuoteQueryParams = Depends()):
#     es = AsyncElasticsearch(
#         "https://192.168.99.100:9200", 
#         basic_auth=("elastic", "P18sc1v5CxZgqh9dhqGC"),
#         verify_certs=False
#     )
#     query_params_json = jsonable_encoder(query_params)
#     match_list = [
#         {"match": {field_name: field_value}} for field_name, field_value in query_params_json.items()
#     ]
#     resp = await es.search(
#         index="index-quotes", 
#         query={
#             "bool": {
#                 "must": match_list
#             }
#         }
#     )
#     return resp
