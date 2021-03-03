from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):

    # help = "Whatever you want to print here"

    def handle(self, **options):
        cache.clear()