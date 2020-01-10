from django.http import JsonResponse
from django.shortcuts import render

from rest_framework import status, viewsets

from main.models import (
    Asset,
    IncomeSource,
    ExpenseCategory,
    IncomeTransaction,
    ExpenseTransaction,
)
from api.exceptions import NotFoundException
from api.permissions import IsAuthenticated, IsOwner
from api.serializers import (
    AssetSerializer,
    IncomeSerializer,
    ExpenseSerializer,
    IncomeTransactionSerializer,
    ExpenseTransactionSerializer,
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


class BaseModelTransactionSet(viewsets.ModelViewSet):
    model_class = None
    serializer_class = None

    queryset = None

    from_field, to_field = "", ""
    from_model, to_model = None, None

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        from_id = request.data.get(self.from_field, {}).get("pk", None)
        to_id = request.data.get(self.to_field, {}).get("pk", None)
        if from_id is None or to_id is None:
            raise NotFoundException()

        from_qs = self.from_model.objects.filter(
            pk=from_id, user=request.user.pk
        ).first()
        to_qs = self.to_model.objects.filter(
            pk=to_id, user=request.user.pk
        ).first()
        if from_qs is None or to_qs is None:
            raise NotFoundException()

        transaction = self.model_class(**serializer.data)
        setattr(transaction, self.from_field, from_qs)
        setattr(transaction, self.to_field, to_qs)
        transaction.save()

        return JsonResponse(
            {"pk": transaction.pk}, status=status.HTTP_201_CREATED
        )


class IncomeTransactionSet(BaseModelTransactionSet):
    model_class = IncomeTransaction
    serializer_class = IncomeTransactionSerializer

    queryset = model_class.objects.select_related().all()

    from_field, to_field = "income", "asset"
    from_model, to_model = IncomeSource, Asset


class ExpenseTransactionSet(BaseModelTransactionSet):
    model_class = ExpenseTransaction
    serializer_class = ExpenseTransactionSerializer

    queryset = model_class.objects.select_related().all()

    from_field, to_field = "asset", "expense"
    from_model, to_model = Asset, ExpenseCategory
