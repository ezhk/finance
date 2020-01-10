from django.http import JsonResponse
from django.shortcuts import render

from rest_framework import status, viewsets

from main.models import Asset, IncomeSource, ExpenseCategory
from api.exceptions import NotFoundException
from api.permissions import IsAuthenticated, IsOwner
from api.serializers import (
    AssetSerializer,
    IncomeSerializer,
    ExpenseSerializer,
)


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
            raise NotFoundException()
        return JsonResponse(
            self.serializer_class(queryset_object, many=True).data, safe=False
        )

    # def retrieve(self, request, pk):
    #     obj = self.queryset.filter(pk=pk, user=request.user.pk).first()
    #     if not obj:
    #         raise NotFoundException()
    #     return JsonResponse(self.serializer_class(obj).data)

    # def update(self, request, pk):
    #     obj = self.queryset.filter(pk=pk, user=request.user.pk).first()
    #     if not obj:
    #         raise NotFoundException()
    #     return super().update(request, pk)

    # def destroy(self, request, pk):
    #     obj = self.queryset.filter(pk=pk, user=request.user.pk).first()
    #     if not obj:
    #         raise NotFoundException()
    #     return super().destroy(request, pk)


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
