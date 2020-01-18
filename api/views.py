from decimal import Decimal

from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from main.models import (
    Asset,
    IncomeSource,
    ExpenseCategory,
    IncomeTransaction,
    ExpenseTransaction,
)
from api.exceptions import NotFoundException, BadRequestException
from api.paginations import PaginationMixin
from api.permissions import IsAuthenticated, IsOwner
from api.serializers import (
    AssetSerializer,
    IncomeSerializer,
    ExpenseSerializer,
    IncomeTransactionSerializer,
    ExpenseTransactionSerializer,
)


class InformationSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Asset.objects.select_related().all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        Method return summary account information, that contains:
        - assets and their balances
        - incomes with summary operations for latest month
        - expenses with summary operations for latest month

        Heavy method with many SQL requests (8 requests),
        of course "created_at" is an indexed field.
        """

        assets = self.queryset.filter(user=request.user)

        # calculate incomes categories for a month
        incomes = IncomeSource.objects.select_related().filter(
            user=request.user
        )
        income_values = IncomeSerializer(incomes, many=True).data
        income_balances = (
            IncomeTransaction.objects.filter(
                asset__user=request.user,
                income__user=request.user,
                created_at__year=timezone.now().year,
                created_at__month=timezone.now().month,
            )
            .values("income")
            .annotate(balance=Sum("amount"))
            .order_by("income")
        )
        for v in income_values:
            v.update(
                income_balances.filter(income=v["pk"])
                .values("balance")
                .first()
                or {"balance": Decimal("0")}
            )

        # calculate expense categories for a month
        expenses = ExpenseCategory.objects.select_related().filter(
            user=request.user
        )
        expense_values = ExpenseSerializer(expenses, many=True).data
        expense_balances = (
            ExpenseTransaction.objects.filter(
                asset__user=request.user,
                expense__user=request.user,
                created_at__year=timezone.now().year,
                created_at__month=timezone.now().month,
            )
            .values("expense")
            .annotate(balance=Sum("amount"))
            .order_by("expense")
        )
        for v in expense_values:
            v.update(
                expense_balances.filter(expense=v["pk"])
                .values("balance")
                .first()
                or {"balance": Decimal("0")}
            )

        return Response(
            {
                "assets": AssetSerializer(assets, many=True).data,
                "incomes": income_values,
                "expenses": expense_values,
            }
        )


class BaseModelSet(viewsets.ModelViewSet, PaginationMixin):
    model_class = None
    serializer_class = None

    queryset = None

    def get_permissions(self):
        """
        Specific method that allow to determine permittion
        classes, they are supported auth and owner checks.
        """

        default_permissions = [IsAuthenticated()]
        if self.action not in ("create", "list"):
            default_permissions.append(IsOwner(model=self.model_class))
        return default_permissions

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        obj = self.model_class(**serializer.data)
        obj.user = request.user
        obj.save()

        return Response(
            self.serializer_class(obj).data, status=status.HTTP_201_CREATED,
        )

    def list(self, request, *args, **kwargs):
        queryset_object = self.queryset.filter(user=request.user.pk)
        if not queryset_object:
            raise NotFoundException()
        page = self.paginate_queryset(self.queryset)
        if page is None:
            raise NotFoundException()

        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)


class BaseModelTransactionSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
    PaginationMixin,
):
    permission_classes = [IsAuthenticated]

    model_class = None
    serializer_class = None

    queryset = None

    from_field, to_field = "", ""
    from_model, to_model = None, None

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            from_id = request.data[self.from_field]["pk"]
            to_id = request.data[self.to_field]["pk"]
        except:
            raise BadRequestException()

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

        return Response({"pk": transaction.pk}, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset_object = self.queryset.filter(
            **{f"{self.from_field}__user": request.user},
            **{f"{self.to_field}__user": request.user},
        )
        if not queryset_object:
            raise NotFoundException()
        page = self.paginate_queryset(queryset_object)
        if page is None:
            raise NotFoundException()
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk):
        obj = self.queryset.filter(
            pk=pk,
            **{f"{self.from_field}__user": request.user},
            **{f"{self.to_field}__user": request.user},
        ).first()
        if not obj:
            raise NotFoundException()
        return Response(self.serializer_class(obj).data)

    def destroy(self, request, pk):
        obj = self.queryset.filter(
            pk=pk,
            **{f"{self.from_field}__user": request.user},
            **{f"{self.to_field}__user": request.user},
        ).first()
        if not obj:
            raise NotFoundException()
        return super().destroy(request, pk)


class AssetSet(BaseModelSet):
    model_class = Asset
    serializer_class = AssetSerializer

    queryset = model_class.objects.select_related().all()

    @action(methods=["get"], detail=True)
    def incoming(self, request, pk):
        incomes = IncomeTransaction.objects.select_related().filter(asset=pk)
        page = self.paginate_queryset(incomes)
        if page is None:
            raise NotFoundException()
        serializer = IncomeTransactionSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=["get"], detail=True)
    def outgoing(self, request, pk):
        expenses = ExpenseTransaction.objects.select_related().filter(asset=pk)
        page = self.paginate_queryset(expenses)
        if page is None:
            raise NotFoundException()
        serializer = ExpenseTransactionSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class IncomeSet(BaseModelSet):
    model_class = IncomeSource
    serializer_class = IncomeSerializer

    queryset = model_class.objects.select_related().all()


class ExpenseSet(BaseModelSet):
    model_class = ExpenseCategory
    serializer_class = ExpenseSerializer

    queryset = model_class.objects.select_related().all()

    @action(methods=["get"], detail=True)
    def incoming(self, request, pk):
        expenses = ExpenseTransaction.objects.select_related().filter(
            expense=pk
        )
        return Response(ExpenseTransactionSerializer(expenses, many=True).data)


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
