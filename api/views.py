from django.http import JsonResponse
from django.shortcuts import render

from rest_framework import status, viewsets
from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission

from main.models import Asset, IncomeSource, ExpenseCategory
from api.serializers import (
    AssetSerializer,
    IncomeSerializer,
    ExpenseSerializer,
)


class ForbiddenException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {
        "error": True,
        "message": "User not authenticated or insufficient roles",
    }
    default_code = "not_authenticated"


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = {"error": True, "message": "Object not found"}
    default_code = "not_found"


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
        query = self.model.objects.filter(
            pk=view.kwargs.get("pk"), user=request.user.pk
        )
        if query.count():
            return True
        raise ForbiddenException()


class BaseModelSet(viewsets.ModelViewSet):
    model_class = None
    serializer_class = None

    queryset = None

    def get_permissions(self):
        """
        Specific method that allow to determine permittion
        classes, they are supported auth and owner checks.
        """

        default_permissions = [IsAuthenticated()]
        if self.action in ("retrieve", "update", "destroy"):
            default_permissions.append(IsOwner(model=self.model_class))
        return default_permissions

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        obj = self.model_class(**serializer.data)
        obj.user = request.user
        obj.save()

        return JsonResponse({"pk": obj.pk}, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset_object = self.queryset.filter(user=request.user.pk)
        if not queryset_object:
            raise NotFound()
        return JsonResponse(
            self.serializer_class(queryset_object, many=True).data, safe=False
        )

    def retrieve(self, request, pk):
        obj = self.queryset.filter(pk=pk, user=request.user.pk).first()
        if not obj:
            raise NotFound()
        return JsonResponse(self.serializer_class(obj).data)

    def update(self, request, pk):
        obj = self.queryset.filter(pk=pk, user=request.user.pk).first()
        if not obj:
            raise NotFound()
        return super().update(request, pk)

    def destroy(self, request, pk):
        obj = self.queryset.filter(pk=pk, user=request.user.pk).first()
        if not obj:
            raise NotFound()
        return super().destroy(request, pk)


class AssetSet(BaseModelSet):
    model_class = Asset
    serializer_class = AssetSerializer

    queryset = model_class.objects.select_related().all()


class IncomeSet(BaseModelSet):
    model_class = IncomeSource
    serializer_class = IncomeSerializer

    queryset = model_class.objects.select_related().all()


class ExpenseSet(BaseModelSet):
    model_class = ExpenseCategory
    serializer_class = IncomeSerializer

    queryset = model_class.objects.select_related().all()
