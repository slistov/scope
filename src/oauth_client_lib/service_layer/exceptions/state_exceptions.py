from typing import Any

from fastapi.exceptions import HTTPException
from fastapi import status

from .generic import InvalidHTTPException


class StateError(InvalidHTTPException):
    """Вернуть общее сообщение об ошибке: {error: state_error}
    
    Добавляет фиксированное сообщение об ошибке к переданному описанию description """
    def __init__(self, description: Any = None) -> None:
        detail = {"error": "state_error"}
        if description:
            detail.update({"description": description})
        super().__init__(detail=detail)


class InvalidState(StateError):
    def __init__(self, description: Any = None) -> None:
        super().__init__(description)


class InactiveState(StateError):
    """Выделить отдельно ситуацию, когда используют неактивный (использованный)  state.
    По бизнес-процессу в этом случае нужно аннулировать авторизацию,
    так как попытка использовать уже использованный state расценивается как атака
    """
    def __init__(self, description: Any = None) -> None:
        super().__init__(description)
