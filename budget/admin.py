from django.contrib import admin
from .models import FinancialStatement, Account, AccuralBudget, CashBudget, Classification, Transaction, CounterPartyTransaction, TransactionTag
from mptt.admin import MPTTModelAdmin
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum


@admin.register(FinancialStatement)
class BudgetFinancialStatementAdmin(admin.ModelAdmin):
    pass


@admin.register(Classification)
class ClassificationAdmin(MPTTModelAdmin):
    list_display = ["__str__",'accural_budgets_value_display']

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
    list_display = ['__str__', 'counter_party_transaction', 'value_display', 'period', 'does_cash_flow_is_correct']
    inlines = [AccuralBudgetInline]

    @admin.display(boolean=True)
    def does_cash_flow_is_correct(self, obj):
        return obj.diff_cash_flow == 0


class AccuralBudgetInline(admin.TabularInline):
    model = AccuralBudget
    extra = 1


class CounterPartyTransactionInline(admin.TabularInline):
    model = CounterPartyTransaction
    extra = 1


@admin.register(CounterPartyTransaction)
class CounterPartyTransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('accural_budgets_value_display',)
    fields = ('transaction', 'counterparty', 'tags', 'accural_budgets_value_display')
    list_display = ['transaction', 'counterparty', 'accural_budgets_value_display', 'tags_display']
    inlines = [AccuralBudgetInline]
    filter_horizontal = ['tags']

    def changelist_view(self, request, extra_context=None):
        # Call the superclass to get the default context
        response = super().changelist_view(request, extra_context=extra_context)
        
        # Get the ChangeList object to access the filtered queryset
        try:
            cl = response.context_data.get('cl')
            if cl:
                # Calculate the total sum of the 'value' field
                total = cl.queryset.aggregate(total=Sum('accural_budgets__value'))['total'] or 0

                # Add the total to the template context
                response.context_data['total'] = f"{total:,}" if total > 0 else f"({abs(total)})"
            
            return response
        except:
            return response


@admin.register(TransactionTag)
class TransactionTagAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['name', 'account', 'accural_budgets_value_display']
    inlines = [CounterPartyTransactionInline]

    def changelist_view(self, request, extra_context=None):
        # Call the superclass to get the default context
        response = super().changelist_view(request, extra_context=extra_context)
        
        # Get the ChangeList object to access the filtered queryset
        try:
            cl = response.context_data.get('cl')
            if cl:
                # Calculate the total sum of the 'value' field
                total = cl.queryset.aggregate(total=Sum('counter_parties__accural_budgets__value'))['total'] or 0

                # Add the total to the template context
                response.context_data['total'] = f"{total:,}" if total > 0 else f"({abs(total)})"
            
            return response
        except:
            return response
        

class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 1


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    readonly_fields = ('accural_budgets_value_display',)
    fields = ('classification', 'name', 'accural_budgets_value_display')
    list_display = ['__str__', 'classification', 'accural_budgets_value_display']
    inlines = [TransactionInline]
