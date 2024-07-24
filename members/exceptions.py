from rest_framework.exceptions import APIException



class ValueError(APIException):
    status_code = 400
    default_detail = 'Bad request'


class DoesNotExist(APIException):
    status_code = 404
    default_detail = 'Object not found'