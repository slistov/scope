from typing import List, Any
from .model_quote import Quote

class Index:
    def __init__(self, index_name, mappings = {}, docs = []) -> None:
        self.index_name = index_name
        self.mappings = mappings
        self.docs = docs