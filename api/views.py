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


class NotAuthenticated(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {"error": True, "message": "User must be authenticated"}
    default_code = "not_authenticated"


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = {"error": True, "message": "Object not found"}
    default_code = "not_found"


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.user.pk is not None:
            return True
        raise NotAuthenticated()


class AssetSet(viewsets.ModelViewSet):
    model_class = Asset
    serializer_class = AssetSerializer

    queryset = model_class.objects.select_related().all()
    permission_classes = [IsAuthenticated]

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


class IncomeSet(AssetSet):
    model_class = IncomeSource
    serializer_class = IncomeSerializer

    queryset = model_class.objects.select_related().all()


class ExpenseSet(AssetSet):
    model_class = ExpenseCategory
    serializer_class = IncomeSerializer

    queryset = model_class.objects.select_related().all()
