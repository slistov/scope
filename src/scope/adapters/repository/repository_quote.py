from ...domain import model
from typing import List
import abc
from elasticsearch.helpers import bulk


class ElasticIndexDocsRepositoryAbstract(abc.ABC):
    def __init__(self) -> None:
        self.docs = []

    def add(self, doc):
        self._add(doc)
        self.docs.append(doc)

    @abc.abstractmethod
    def _add(self, doc):
        raise NotImplementedError


class ElasticIndexDocsRepository(ElasticIndexDocsRepositoryAbstract):
    def __init__(self, index) -> None:
        super.__init__()
        self.index.bul

    def _add(self, doc):
        self.index.

