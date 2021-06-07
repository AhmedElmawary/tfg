from rest_framework.exceptions import APIException


class HttpError(APIException):
    status_code = None

    def __init__(self, detail=None, code=None, status=None):
        self.status_code = status
        return super(HttpError, self).__init__(detail, code)
