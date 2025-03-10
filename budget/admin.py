from django.contrib import admin
from .models import FinancialStatement, Account, AccuralBudgetValue, CashBudgetValue, Classification
from mptt.admin import MPTTModelAdmin

@admin.register(FinancialStatement)
class FinancialStatementAdmin(admin.ModelAdmin):
    pass

@admin.register(Classification)
class ClassificationAdmin(MPTTModelAdmin):
    pass

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'classification']

@admin.register(AccuralBudgetValue)
class AccuralBudgetValueAdmin(admin.ModelAdmin):
    pass

@admin.register(CashBudgetValue)
class CashBudgetValueAdmin(admin.ModelAdmin):
    pass