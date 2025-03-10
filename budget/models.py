from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from mptt.models import MPTTModel, TreeForeignKey


class FinancialStatement(models.Model):
    name = models.CharField(_("name"), max_length=255)

    def __str__(self):
        return self.name
    

class Classification(MPTTModel):
    financial_statement = models.ForeignKey(FinancialStatement, on_delete=models.SET_NULL, blank=True, null=True, related_name="financial_statements")
    name = models.CharField(_("name"), max_length=255)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Account(models.Model):
    classification = models.ForeignKey(Classification, on_delete=models.SET_NULL, blank=True, null=True, related_name="accounts")
    name = models.CharField(_("name"), max_length=255)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


# class CashAccount(models.Model):
#     classification = models.ForeignKey(Classification, on_delete=models.SET_NULL, blank=True, null=True, related_name="accounts")
#     name = models.CharField(_("name"), max_length=255)

#     class MPTTMeta:
#         order_insertion_by = ['name']

#     def __str__(self):
#         return self.name


class BudgetValue(models.Model):
    value = models.PositiveBigIntegerField(_("value"))
    month = models.PositiveIntegerField(_("number"), validators=[MaxValueValidator(12), MinValueValidator(1)])
    year = models.PositiveIntegerField(_("number"))

    def period(self):
        month = self.month
        converted_month = str(month) if month >= 10 else f"0{month}"
        return f"{self.year}{converted_month}"

    class Meta:
        abstract = True


class AccuralBudgetValue(BudgetValue):
    account = models.ForeignKey(Account, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.account.name} {self.value} {self.period()}"


class CashBudgetValue(BudgetValue):
    budget_value = models.ForeignKey(AccuralBudgetValue, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.budget_value.account.name} {self.value} {self.period()}"