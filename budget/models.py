from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from mptt.models import MPTTModel, TreeForeignKey
from colifelabs_management.utils import accounting_display

class FinancialStatement(models.Model):
    name = models.CharField(_("name"), max_length=255)
    slug = models.SlugField(_("slug"), unique=True)
    material_ui_icon = models.CharField(_("Material UI icon"), max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
    

class Classification(MPTTModel):
    financial_statement = models.ForeignKey(FinancialStatement, on_delete=models.SET_NULL, blank=True, null=True, related_name="classifications")
    name = models.CharField(_("name"), max_length=255)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    sibiling_order = models.SmallIntegerField(_("sibiling order"), default=0)

    @property
    def accural_budgets_value(self):
        childrens_v = sum([c.accural_budgets_value for c in self.children.all()])
        accounts_v = sum([a.accural_budgets_value for a in self.accounts.all()])
        return childrens_v + accounts_v

    @property
    def accural_budgets_value_display(self):
        return accounting_display(self.accural_budgets_value)

    def __str__(self):
        return self.name
    
    class MPTTMeta:
        order_insertion_by = ['name']


class Account(models.Model):
    classification = models.ForeignKey(Classification, on_delete=models.SET_NULL, blank=True, null=True, related_name="accounts")
    name = models.CharField(_("name"), max_length=255)

    @property
    def accural_budgets_value(self):
        return sum([t.accural_budgets_value for t in self.transactions.all()])
  
    @property
    def accural_budgets_value_display(self):
        return accounting_display(self.accural_budgets_value)

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']


class TransactionTag(models.Model):
    name = models.CharField(_("name"), max_length=255)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    name = models.CharField(_("name"), max_length=255)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="transactions")

    @property
    def accural_budgets_value(self):
        return sum([cp.accural_budgets_value for cp in self.counter_parties.all()])

    @property
    def accural_budgets_value_display(self):
        return accounting_display(self.accural_budgets_value)

    def __str__(self):
        return self.name


class CounterPartyTransaction(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT, related_name="counter_parties")
    counterparty = models.ForeignKey("ecosystem.Counterparty", on_delete=models.PROTECT, related_name="transactions")
    tags = models.ManyToManyField(TransactionTag, blank=True, related_name="transactions")

    @property
    def accural_budgets_value(self):
        return sum([bv.value for bv in self.accural_budgets.all()])

    @property
    def accural_budgets_value_display(self):
        return accounting_display(self.accural_budgets_value)

    @property
    def tags_display(self):
        return " - ".join([t.name for t in self.tags.all()])
    
    def __str__(self):
        return f"{self.transaction.name} {self.counterparty}"


class Budget(models.Model):
    value = models.BigIntegerField(_("value"), default=0)
    month = models.PositiveIntegerField(_("month"), validators=[MaxValueValidator(12), MinValueValidator(1)])
    year = models.PositiveIntegerField(_("year"))

    @property
    def period(self):
        month = self.month
        converted_month = str(month) if month >= 10 else f"0{month}"
        return f"{self.year}{converted_month}"

    @property
    def value_display(self):
        return accounting_display(self.value)

    class Meta:
        abstract = True


class AccuralBudget(Budget):
    counter_party_transaction = models.ForeignKey(CounterPartyTransaction, on_delete=models.PROTECT, related_name="accural_budgets")
    
    @property
    def diff_cash_flow(self):
        return self.value - sum([cf.value for cf in self.cash_flows.all()])

    @property
    def diff_cash_flow_display(self):
        return accounting_display(self.diff_cash_flow)

    def __str__(self):
        return f"{self.counter_party_transaction.transaction.account.name} {self.period}"


class CashBudget(Budget):
    budget_value = models.ForeignKey(AccuralBudget, on_delete=models.PROTECT, related_name="cash_flows")

    def __str__(self):
        value_display = accounting_display(self.value)
        return f"{self.budget_value.counter_party_transaction.transaction.account.name} {value_display} {self.period}"