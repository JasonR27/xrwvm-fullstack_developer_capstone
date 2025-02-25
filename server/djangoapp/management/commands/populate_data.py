from django.core.management.base import BaseCommand
from djangoapp.populate import initiate


class Command(BaseCommand):
    help = 'Populate MongoDB with initial data'

    def handle(self, *args, **kwargs):
        initiate()
        self.stdout.write(self.style.SUCCESS(
            'Database populated successfully'))
