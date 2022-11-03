from pydantic import BaseModel

class Quote(BaseModel):
    movie: str
    speaker: str
    quote_eng: str
    quote_rus: str
    stuff: str   