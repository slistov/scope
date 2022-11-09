from typing import Any, List

from .model_quote import Quote
from ..mappings.quote import quote_mapping



class Index:
    def __init__(self, index_name, mappings = {}, docs = []) -> None:
        self.index_name = index_name
        self.mappings = mappings
        self.docs = docs


class IndexQuote(Index):
    def __init__(self, index_name, docs=[]) -> None:
        super().__init__(index_name, quote_mapping, docs)