from django.urls import path, include
from rest_framework import routers

from api.views import (
    InformationSet,
    AssetSet,
    IncomeSet,
    ExpenseSet,
    IncomeTransactionSet,
    ExpenseTransactionSet,
)

router = routers.SimpleRouter()
router.register(r"common-info", InformationSet)
router.register(r"assets", AssetSet)
router.register(r"incomes", IncomeSet)
router.register(r"expenses", ExpenseSet)
router.register(r"income-transactions", IncomeTransactionSet)
router.register(r"expense-transactions", ExpenseTransactionSet)

app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
]
