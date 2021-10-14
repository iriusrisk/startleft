from typing import List

from pydantic import BaseModel


class ErrorResponseItem(BaseModel):
    errorMessage: str

    def __init__(self, error_message: str):
        super().__init__(errorMessage=error_message)


class ErrorResponse(BaseModel):
    status: str
    errors: List[ErrorResponseItem] = []

    def __init__(self, status: str, messages: List[str]):
        items = []
        for message in messages:
            items.append(ErrorResponseItem(message))

        super().__init__(status=status, errors=items)
