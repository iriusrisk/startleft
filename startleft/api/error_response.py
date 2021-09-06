from typing import List

from pydantic import BaseModel


class ErrorResponseMessage(BaseModel):
    type: str

    def __init__(self, type: str):
        super().__init__(type=type)


class ErrorResponseItem(BaseModel):
    item: ErrorResponseMessage

    def __init__(self, item: ErrorResponseMessage):
        super().__init__(item=item)


class ErrorResponse(BaseModel):
    status: int
    errors: List[ErrorResponseItem] = []

    def __init__(self, status: int, message_type: str):
        message = ErrorResponseMessage(message_type)
        item = ErrorResponseItem(message)

        super().__init__(status=status, errors=[item])
