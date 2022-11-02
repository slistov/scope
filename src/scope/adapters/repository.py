from ..domain import model
from typing import List

class QuoteElasticRepository:
    quotes: List[model.Quote]
    def __init__(self) -> None:
        pass

    def add(self, quote: model.Quote):
        self.quotes.append(quote)
    
    def get_quotes_by_substr(self, substr: str) -> List[model.Quote]:
        return [quote for quote in self.quotes if substr in quote]