from django.urls import path, include
from rest_framework import routers

from api.views import AssetSet, IncomeSet, ExpenseSet

router = routers.SimpleRouter()
router.register(r"assets", AssetSet)
router.register(r"incomes", IncomeSet)
router.register(r"expenses", ExpenseSet)
# router.register(r"income-transactions", IncomeTransactionSet)
# router.register(r"expense-transactions", ExpenseTransactionSet)

app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
]
