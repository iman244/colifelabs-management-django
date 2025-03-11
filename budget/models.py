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


class TransactionTag(models.Model):
    name = models.CharField(_("name"), max_length=255)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    name = models.CharField(_("name"), max_length=255)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="transactions")
    tags = models.ManyToManyField(TransactionTag, related_name="transactions")

    def accural_budgets_value(self):
        return sum([cp.accural_budgets_value() for cp in self.counter_parties.all()])

    def accural_budgets_value_display(self):
        return f"{self.accural_budgets_value():,}"
    
    def tags_display(self):
        return " - ".join([t.name for t in self.tags])

    def __str__(self):
        return self.name


class CounterPartyTransaction(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT, related_name="counter_parties")
    counterparty_tag = models.ForeignKey("ecosystem.CounterpartyTag", on_delete=models.PROTECT, related_name="transactions")

    def accural_budgets_value(self):
        return sum([bv.value for bv in self.accural_budgets.all()])

    def accural_budgets_value_display(self):
        return f"{self.accural_budgets_value():,}"

    def __str__(self):
        return f"{self.transaction.name} {self.counterparty_tag}"


class Budget(models.Model):
    value = models.PositiveBigIntegerField(_("value"))
    month = models.PositiveIntegerField(_("month"), validators=[MaxValueValidator(12), MinValueValidator(1)])
    year = models.PositiveIntegerField(_("year"))

    def period(self):
        month = self.month
        converted_month = str(month) if month >= 10 else f"0{month}"
        return f"{self.year}{converted_month}"
    
    def value_display(self):
        return f"{self.value:,}"

    class Meta:
        abstract = True


class AccuralBudget(Budget):
    counter_party_transaction = models.ForeignKey(CounterPartyTransaction, on_delete=models.PROTECT, related_name="accural_budgets")
    
    def diff_cash_flow(self):
        return self.value - sum([cf.value for cf in self.cash_flows.all()])

    def diff_cash_flow_display(self):
        return f"{self.diff_cash_flow():,}"

    def __str__(self):
        return f"{self.counter_party_transaction.transaction.account.name} {self.value:,} {self.period()}"


class CashBudget(Budget):
    budget_value = models.ForeignKey(AccuralBudget, on_delete=models.PROTECT, related_name="cash_flows")

    def __str__(self):
        return f"{self.budget_value.counter_party_transaction.transaction.account.name} {self.value:,} {self.period()}"