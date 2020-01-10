from rest_framework import serializers
from main.models import Asset, IncomeSource, ExpenseCategory


class AssetSerializer(serializers.ModelSerializer):
    explained_type = serializers.CharField(
        source="get_type_display", read_only=True
    )

    class Meta:
        model = Asset
        fields = ("description", "balance", "type", "explained_type")


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeSource
        fields = ("description",)


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ("description", "monthly_limit")
