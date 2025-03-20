from rest_framework import serializers
from .models import FinancialStatement, Classification, Account, Transaction, CounterPartyTransaction, AccuralBudget


class AccuralBudgetSerializer(serializers.ModelSerializer):
    period = serializers.ReadOnlyField()

    class Meta:
        model = AccuralBudget
        exclude = ['counter_party_transaction']


class CounterPartyTransactionSerializer(serializers.ModelSerializer):
    accural_budgets = AccuralBudgetSerializer(many=True, read_only=True)
    accural_budgets_value = serializers.ReadOnlyField()
    class Meta:
        model = CounterPartyTransaction
        exclude = ['transaction', 'counterparty']


class TransactionSerializer(serializers.ModelSerializer):
    counter_parties = CounterPartyTransactionSerializer(many=True, read_only=True)
    accural_budgets_value = serializers.ReadOnlyField()

    class Meta:
        model = Transaction
        exclude = ['account']


class AccountSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)
    accural_budgets_value = serializers.ReadOnlyField()

    class Meta:
        model = Account
        exclude = ['classification']


class ClassificationSerializer(serializers.ModelSerializer):
    accounts = AccountSerializer(many=True, read_only=True)
    accural_budgets_value = serializers.ReadOnlyField()

    class Meta:
        model = Classification
        exclude = ['financial_statement']


class FinancialStatementSerializer(serializers.ModelSerializer):
    classifications = ClassificationSerializer(many=True, read_only=True)

    class Meta:
        model = FinancialStatement
        fields = '__all__'