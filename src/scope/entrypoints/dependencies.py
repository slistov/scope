from typing import List

from fastapi import Depends, Header, HTTPException

from ..service_layer import services
from ..adapters.repository import ElasticIndexRepository
from .. import config
from elasticsearch import AsyncElasticsearch

user, password = config.get_es_user_credentials()
es = AsyncElasticsearch(
    config.get_es_uri(), 
    basic_auth=(user, password),
    verify_certs=False
)

elastic_repo = ElasticIndexRepository(es)


async def get_query_token(access_token: str = Header()):
    if not access_token:
        raise HTTPException(status_code=400, detail="No access_token provided!")
    return access_token


async def get_token_oauthService_validated(token: str = Depends(get_query_token)):
    oauth_requester = services.OauthRequester()
    if not oauth_requester.validate_token(token):
        raise HTTPException(status_code=400, detail="access_token header invalid")
    return oauth_requester.scopes[token]


async def token_scopes_read_write(scopes: List = Depends(get_token_oauthService_validated)):
    return scopes == ['read', 'write']


