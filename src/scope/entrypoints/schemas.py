from typing import Optional

from fastapi import Query
from pydantic import BaseModel


class Quote(BaseModel):
    movie: str
    speaker: str
    quote_rus: str
    stuff: str   


class QuoteQueryParams:
    def __init__(
        self,
        movie: str = Query(None),
        speaker: str = Query(None),
        quote_rus: str = Query(None),
        stuff: str = Query(None)
    ) -> None:
        if movie:
            self.movie = movie
        if speaker:
            self.speaker = speaker
        if quote_rus:
            self.quote_rus = quote_rus
        if stuff:
            self.stuff = stuff
    