import json

class IriusUnauthorizedError(Exception):
    status_code = 401

class IriusTokenError(Exception):
    status_code = 401


class IriusServerError(Exception):
    status_code = 500


class IriusApiError(Exception):
    pass
    # status_code: int
    # message: str
    # response: str
    #
    # def __init__(self, status_code: int, message: str, response: str):
    #     self.status_code = status_code
    #     self.message = message
    #     self.response = response
    #
    # def get_error_response(self):
    #     try:
    #         json.dumps(self.response, indent=2)
    #     except Exception:
    #         self.message = "manolo"
    #
    #     return self.message
