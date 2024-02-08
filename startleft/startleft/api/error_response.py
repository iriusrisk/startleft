from typing import List

from pydantic import BaseModel


class ErrorResponseItem(BaseModel):
    errorMessage: str

    def __init__(self, error_message: str):
        super().__init__(errorMessage=error_message)


class ErrorResponse(BaseModel):
    status: str
    error_type: str
    title: str
    detail: str
    errors: List[ErrorResponseItem] = []

    def __init__(self, status: str,  error_type: str,  title: str,  detail: str, messages: List[str]):
        items = []
        if messages:
            for message in messages:
                items.append(ErrorResponseItem(message))
        super().__init__(status=status, error_type=str(error_type), title=title, detail=detail, errors=items)
