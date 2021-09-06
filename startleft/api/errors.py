
class IriusTokenError(Exception):
    status_code = 403


class IriusServerError(Exception):
    status_code = 500


class IriusApiError(Exception):
    status_code = 500