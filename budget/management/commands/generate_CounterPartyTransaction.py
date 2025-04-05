from django.core.management.base import BaseCommand
from budget.models import CounterPartyTransaction, Transaction, AccuralBudget

class Command(BaseCommand):
    help = "Generate Insurance expense"

    def add_arguments(self, parser):
        parser.add_argument("src_transaction_id", nargs=1, type=int)
        parser.add_argument("target_transaction_id", nargs=1, type=int)
        parser.add_argument("percent", nargs=1, type=int)

    def handle(self, *args, **options):
        print("args", args)
        print("options", options)
        src_transaction_id = options['src_transaction_id'][0]
        target_transaction_id = options['target_transaction_id'][0]
        percent = options['percent'][0]

        src_transaction = Transaction.objects.get(pk=src_transaction_id)
        target_transaction = Transaction.objects.get(pk=target_transaction_id)

        print("src_transaction", src_transaction,)
        print("target_transaction", target_transaction,)

        srcCounterPartyTransactions = CounterPartyTransaction.objects.filter(transaction=src_transaction)

        for cp in srcCounterPartyTransactions:
            newCp, created = CounterPartyTransaction.objects.get_or_create(transaction=target_transaction, counterparty=cp.counterparty)
            self.stdout.write(self.style.SUCCESS(f"-- created: {created} {newCp}"))
            for accural_budget in cp.accural_budgets.all():
                val = accural_budget.value * percent / 100
                newAccB, created_newAccB = AccuralBudget.objects.get_or_create(counter_party_transaction=newCp, year=accural_budget.year, month=accural_budget.month, value=val)
                self.stdout.write(self.style.SUCCESS(f"    created: {created_newAccB} {newAccB}"))
