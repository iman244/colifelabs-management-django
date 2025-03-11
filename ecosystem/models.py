from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CounterpartyTag(models.Model):
    name = models.CharField(_("name"), max_length=255)

    def total_accural_budget(self):
        return sum([cpt.accural_budgets_value() for cpt in self.transactions.all()])
    
    def total_accural_budget_display(self):
        return f"{self.total_accural_budget():,}"

    def __str__(self):
        return self.name


class Counterparty(models.Model):
    tag = models.ForeignKey(CounterpartyTag, on_delete=models.SET_NULL, blank=True, null=True, related_name="counterparties")
    name = models.CharField(_("name"), max_length=255)

    def __str__(self):
        return self.name