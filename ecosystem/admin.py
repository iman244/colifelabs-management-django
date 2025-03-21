from django.contrib import admin
from .models import Counterparty, CounterpartyTag
from budget.admin import CounterPartyTransactionInline


@admin.register(Counterparty)
class CounterpartyAdmin(admin.ModelAdmin):
    list_display = ["__str__", 'total_accural_budget_display']
    inlines = [CounterPartyTransactionInline]


@admin.register(CounterpartyTag)
class CounterpartyTagAdmin(admin.ModelAdmin):
    list_display = ["__str__", 'total_accural_budget_display']