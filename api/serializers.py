from rest_framework import serializers
from main.models import (
    Asset,
    IncomeSource,
    ExpenseCategory,
    IncomeTransaction,
    ExpenseTransaction,
)


class AssetSerializer(serializers.ModelSerializer):
    explained_type = serializers.CharField(
        source="get_type_display", read_only=True
    )

    class Meta:
        model = Asset
        fields = ("pk", "description", "balance", "type", "explained_type")


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeSource
        fields = ("pk", "description")


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ("pk", "description", "monthly_limit")


class IncomeTransactionSerializer(serializers.ModelSerializer):
    asset = AssetSerializer(read_only=True)
    income = IncomeSerializer(read_only=True)

    class Meta:
        model = IncomeTransaction
        fields = "__all__"


class ExpenseTransactionSerializer(serializers.ModelSerializer):
    asset = AssetSerializer(read_only=True)
    expense = ExpenseSerializer(read_only=True)

    class Meta:
        model = ExpenseTransaction
        fields = "__all__"
