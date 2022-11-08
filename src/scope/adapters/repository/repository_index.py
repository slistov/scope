from ...domain import model
from typing import List
import abc 
from elasticsearch import Elasticsearch

class ElasticIndexRepositoryAbstract(abc.ABC):
    def __init__(self) -> None:
        self.docs = []

    def add(self, index: model.Index):
        self._add(index)
    
    def get_index_by_name(self, index_name) -> model.Index:
        return self._get_index_by_name(index_name)

    @abc.abstractmethod
    def _add(self, index: model.Index):
        raise NotImplementedError
    
    @abc.abstractmethod
    def _get_index_by_name(self, index_name) -> model.Index:
        raise NotImplementedError
    


class ElasticIndexRepository(ElasticIndexRepositoryAbstract):
    def __init__(self, elasticsearch: Elasticsearch) -> None:
        super().__init__()
        self.elasticsearch = elasticsearch

    def _add(self, index: model.Index):
        self.elasticsearch.indices.create(index=index.index_name, mappings=index.mappings)
    
    def _get_index_by_name(self, index_name) -> model.Index:
        return self.elasticsearch.indices.get(index=index_name)
