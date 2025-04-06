from django.core.management.base import BaseCommand
from budget.models import CounterPartyTransaction, Transaction, AccuralBudget
from colifelabs_management.settings import BASE_DIR
import pandas as pd

class Command(BaseCommand):
    help = "Generate Insurance expense"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", nargs=1, type=str)
        
    def handle(self, *args, **options):
        print("args", args)
        print("options", options)
        csv_file_path = BASE_DIR / options['csv_file'][0]
        print("csv_file_path", csv_file_path)
        df = pd.read_csv(csv_file_path)
        print("df", df)