from rest_framework import status
from rest_framework.exceptions import APIException


class ForbiddenException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {
        "error": True,
        "message": "User not authenticated or insufficient roles",
    }
    default_code = "not_authenticated"


class NotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = {"error": True, "message": "Object not found"}
    default_code = "not_found"
