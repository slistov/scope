import abc
from typing import List

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from ...domain import model


class ElasticIndexRepositoryAbstract(abc.ABC):
    async def add(self, index: model.Index):
        await self._add(index)
    
    async def get_index_by_name(self, index_name) -> model.Index:
        return await self._get_index_by_name(index_name)
    
    async def add_docs_bulk(self, index_name, docs_bulk):
        await self._add_docs_bulk(index_name, docs_bulk)

    async def search(self, index_name, text):
        return await self._search(index_name, text)

    @abc.abstractmethod
    def _add(self, index: model.Index):
        raise NotImplementedError

    @abc.abstractmethod
    def _add_docs_bulk(self, index_name, docs_bulk):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_index_by_name(self, index_name) -> model.Index:
        raise NotImplementedError
    
    async def _search(self, index_name, text):
        raise NotImplementedError


class ElasticIndexRepository(ElasticIndexRepositoryAbstract):
    def __init__(self, elasticsearch: AsyncElasticsearch) -> None:
        self.elasticsearch = elasticsearch

    async def _add(self, index: model.Index):
        await self.elasticsearch.indices.create(index=index.index_name, mappings=index.mappings)
    
    async def _get_index_by_name(self, index_name) -> model.Index:
        return await self.elasticsearch.indices.get(index=index_name)
    
    async def _add_docs_bulk(self, index_name, docs_bulk):
        try:
            result = await async_bulk(self.elasticsearch, docs_bulk, index=index_name)
            return result
        except Exception as e:
            return False
    
    async def _search(self, index_name, text):
        return await self.elasticsearch.search(index=index_name, query={"match": {"quote": text}})


