from django.contrib import admin
from .models import FinancialStatement, Account, AccuralBudget, CashBudget, Classification, Transaction, CounterPartyTransaction
from mptt.admin import MPTTModelAdmin
from django.utils.translation import gettext_lazy as _

@admin.register(FinancialStatement)
class FinancialStatementAdmin(admin.ModelAdmin):
    pass


@admin.register(Classification)
class ClassificationAdmin(MPTTModelAdmin):
    pass


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'classification']


# @admin.register(CashBudget)
# class CashBudgetAdmin(admin.ModelAdmin):
#     pass


class AccuralBudgetInline(admin.TabularInline):
    model = CashBudget
    extra = 1


@admin.register(AccuralBudget)
class AccuralBudgetAdmin(admin.ModelAdmin):
    readonly_fields = ("value_display", "diff_cash_flow_display",)
    fields =  ("counter_party_transaction", "value", "month", "year", "value_display", "diff_cash_flow_display")
    list_display = ['counter_party_transaction', 'value_display', 'period', 'does_cash_flow_is_correct']
    inlines = [AccuralBudgetInline]

    @admin.display(boolean=True)
    def does_cash_flow_is_correct(self, obj):
        return obj.diff_cash_flow() == 0


class AccuralBudgetInline(admin.TabularInline):
    model = AccuralBudget
    extra = 1


class CounterPartyTransactionInline(admin.TabularInline):
    model = CounterPartyTransaction
    extra = 1


@admin.register(CounterPartyTransaction)
class CounterPartyTransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction', 'counterparty_tag', 'accural_budgets_value_display']
    inlines = [AccuralBudgetInline]

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['name', 'account', 'accural_budgets_value_display']
    inlines = [CounterPartyTransactionInline]