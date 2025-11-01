# abcstracts/management/commands/seeders.py
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Ejecuta todos los seeders'

    def handle(self, *args, **options):
        self.stdout.write(' Ejecutando seeders...')
        
        call_command('seeders_categories')
        call_command('seeders_permisions')
        call_command('seeders_groups')
        call_command('seeder_user')
        
        self.stdout.write(self.style.SUCCESS('Todos los seeders ejecutados correctamente'))