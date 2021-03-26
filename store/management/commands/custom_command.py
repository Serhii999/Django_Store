from django.core.management.base import BaseCommand
from store.models import *



class Command(BaseCommand):
    help = "Close orders which weren't closed manually"

    def handle(self, *args, **options):
        returns = ReturnPurchase.objects.all()
        if returns:
            returns.all().delete()
