from django.db import models
from django.utils.translation import gettext_lazy as _
from colifelabs_management.utils import accounting_display


class CounterpartyTag(models.Model):
    name = models.CharField(_("name"), max_length=255)

    @property
    def total_accural_budget(self):
        return sum([cpt.accural_budgets_value for cpt in self.transactions.all()])
    
    @property
    def total_accural_budget_display(self):
        return accounting_display(self.total_accural_budget)
    
    def __str__(self):
        return self.name


class Counterparty(models.Model):
    tag = models.ForeignKey(CounterpartyTag, on_delete=models.SET_NULL, blank=True, null=True, related_name="counterparties")
    name = models.CharField(_("name"), max_length=255)

    @property
    def total_accural_budget(self):
        return sum([t.accural_budgets_value for t in self.transactions.all()])
    
    @property
    def total_accural_budget_display(self):
        return accounting_display(self.total_accural_budget)
    
    def __str__(self):
        return self.name