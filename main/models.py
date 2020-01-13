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


class IncomeTransaction(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    income = models.ForeignKey(IncomeSource, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    amount = models.DecimalField(
        verbose_name="Income money amount",
        blank=False,
        default=0,
        max_digits=19,
        decimal_places=4,
    )

    def save(self, *args, **kwargs):
        """
        Redefine standart save method,
        because need to change asset balance at first.
        """

        with transaction.atomic():
            self.asset.balance += Decimal(self.amount)
            self.asset.save()

            super().save(*args, **kwargs)
        return True

    def delete(self):
        """
        Redefine standart delete method,
        because need to change asset balance at first.
        """

        with transaction.atomic():
            self.asset.balance -= Decimal(self.amount)
            self.asset.save()

            super().delete()
        return True

    class Meta:
        ordering = ("-created_at",)


class ExpenseTransaction(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    expense = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    amount = models.DecimalField(
        verbose_name="Expense maney amount",
        blank=False,
        default=0,
        max_digits=19,
        decimal_places=4,
    )
    tags = models.CharField(
        verbose_name="Comma separated transaction tags",
        max_length=4096,
        null=True,
        blank=True,
        default="",
    )

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.asset.balance -= Decimal(self.amount)
            self.asset.save()

            super().save(*args, **kwargs)
        return True

    def delete(self):
        with transaction.atomic():
            self.asset.balance += Decimal(self.amount)
            self.asset.save()

            super().delete()
        return True

    class Meta:
        ordering = ("-created_at",)
