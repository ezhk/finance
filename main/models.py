from decimal import Decimal

from django.conf import settings
from django.db import models, transaction


class IncomeSource(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    description = models.CharField(
        verbose_name="Income source description", max_length=2048, blank=False,
    )


class Asset(models.Model):
    """
    Class describe account fields,
      contains total money amount with Decimal presition
      and kind of asset, like a bank card, credit card and cash.

    https://stackoverflow.com/questions/224462/storing-money-in-a-decimal-column-what-precision-and-scale/224866#224866
    """

    CASH, BANK_CARD, CREDIT_CARD = "CA", "BC", "CC"
    ASSET_CHOICES = [
        (CASH, "Cash"),
        (BANK_CARD, "Bank card"),
        (CREDIT_CARD, "Credit card"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    description = models.CharField(
        verbose_name="Asset category description",
        max_length=2048,
        blank=False,
    )
    balance = models.DecimalField(
        verbose_name="Current money balance",
        blank=False,
        default=0,
        max_digits=19,
        decimal_places=4,
    )
    type = models.CharField(
        verbose_name="Type of asset",
        max_length=2,
        choices=ASSET_CHOICES,
        blank=True,
    )
    image = models.ImageField(
        verbose_name="Asset image preview",
        upload_to="asset-images",
        blank=True,
    )


class ExpenseCategory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    description = models.CharField(
        verbose_name="Expense category description",
        max_length=2048,
        blank=False,
    )
    monthly_limit = models.FloatField(
        verbose_name="Monthly expenses limit", null=True, default=None
    )
    image = models.ImageField(
        verbose_name="Expense image preview",
        upload_to="expense-images",
        blank=True,
    )


class AbstractTransaction(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    amount = models.DecimalField(
        verbose_name="Transaction maney amount",
        blank=False,
        default=0,
        max_digits=19,
        decimal_places=4,
    )

    def inc_asset(self, value):
        """
        Increment asset balance on input value.
        """
        self.asset.balance += Decimal(value)
        self.asset.save()

    def dec_asset(self, value):
        """
        Decrement asset balance on input value.
        """
        self.asset.balance -= Decimal(value)
        self.asset.save()

    class Meta:
        abstract = True
        ordering = ("-created_at",)


class IncomeTransaction(AbstractTransaction):
    income = models.ForeignKey(IncomeSource, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """
        Redefine standart save method,
        because need to change asset balance at first.
        """

        with transaction.atomic():
            self.inc_asset(self.amount)
            super().save(*args, **kwargs)
        return True

    def delete(self):
        """
        Redefine standart delete method,
        because need to change asset balance at first.
        """

        with transaction.atomic():
            self.dec_asset(self.amount)
            super().delete()
        return True


class ExpenseTransaction(AbstractTransaction):
    expense = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    tags = models.CharField(
        verbose_name="Comma separated transaction tags",
        max_length=4096,
        null=True,
        blank=True,
        default="",
    )

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.dec_asset(self.amount)
            super().save(*args, **kwargs)
        return True

    def delete(self):
        with transaction.atomic():
            self.inc_asset(self.amount)
            super().delete()
        return True


class FabricTransaction:
    INCOME = "IncomeTransaction"
    EXPENSE = "ExpenseTransaction"

    @staticmethod
    def create_factory(name, *args, **kwargs):
        if name == __class__.INCOME:
            return globals()[__class__.INCOME]()
        if name == __class__.EXPENSE:
            return globals()[__class__.EXPENSE]()


class TransactionBuilder:
    def __init__(self, transaction_type):
        self._transaction = FabricTransaction.create_factory(transaction_type)

    def asset(self, asset_id):
        self._transaction.asset_id = asset_id
        return self

    def amount(self, amount):
        self._transaction.amount = amount
        return self

    def build(self):
        return self._transaction


"""
FabricTransaction and TransactionBuilder
presented as a demostration to lesson 3
of homework:
- FabricTransaction is a fibric method for created
  transaction instance
- TransactionBuilder add diferent attributes to
  object

How does it work:
>>> from main.models import *
>>> obj = TransactionBuilder("IncomeTransaction")
>>> Asset.objects.first().id
1
>>> obj.asset(1)
<main.models.TransactionBuilder object at 0x10271e150>
>>> obj.amount(100500)
<main.models.TransactionBuilder object at 0x10271e150>
>>> builded_transaction = obj.asset(1).amount(100500).build()
>>> builded_transaction.__dict__
{'_state': <django.db.models.base.ModelState object at 0x102719dd0>, 'id': None, 'asset_id': 1, 'created_at': None, 'amount': 100500, 'income_id': None}
>>> builded_transaction.save()
...
sqlite3.IntegrityError: NOT NULL constraint failed: main_incometransaction.income_id
...
>>> builded_transaction.income_id = 1
>>> builded_transaction.save()
True
>>> builded_transaction.pk
2

Result:
>>> IncomeTransaction.objects.get(pk=2).__dict__
{'_state': <django.db.models.base.ModelState object at 0x1028a8390>, 'id': 2, 'asset_id': 1, 'created_at': datetime.datetime(2020, 1, 22, 7, 44, 46, 458567, tzinfo=<UTC>), 'amount': Decimal('100500.0000'), 'income_id': 1}
"""
