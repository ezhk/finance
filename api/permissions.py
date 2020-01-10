from rest_framework.permissions import BasePermission

from api.exceptions import ForbiddenException, NotFoundException


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.user.pk is not None:
            return True
        raise ForbiddenException()


class IsOwner(BasePermission):
    """
    Class using in BaseModelSet for user owner validation.
    """

    def __init__(self, **kwargs):
        self.model = kwargs.get("model")
        super().__init__()

    def has_permission(self, request, view):
        obj = (
            self.model.objects.select_related()
            .filter(pk=view.kwargs.get("pk"))
            .first()
        )

        # don't need permission for empty object
        if obj is None:
            return NotFoundException()

        if obj.user == request.user:
            return True

        raise ForbiddenException()
