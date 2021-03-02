from django.core.management.base import BaseCommand
from rides.models import Status

class Command(BaseCommand):

    # help = "Whatever you want to print here"

    
    def handle(self, **options):
        Status.objects.all().delete()
        Status.objects.create(name='On Queue', color='#007bff')
        Status.objects.create(name='Ongoing', color='#28a745')
        Status.objects.create(name='Completed', color='#28a745')
        Status.objects.create(name='Cancelled', color='#00000')
        print(Status.objects.all())