from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied


class PermissionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Allow only auth methods for anonymous users:
        class validate user instance and check URI path.
        """

        if isinstance(
            request.user, AnonymousUser
        ) and not request.path.startswith("/rest-auth/"):
            raise PermissionDenied()

        response = self.get_response(request)
        return response
