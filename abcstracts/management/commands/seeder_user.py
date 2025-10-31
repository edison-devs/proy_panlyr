# core/management/commands/seed_root_user.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from core.models import User

class Command(BaseCommand):
    help = 'Create root user'

    def handle(self, *args, **options):
        self.stdout.write('Creating root user...')
        
        self.create_root_user()
        
        self.stdout.write(self.style.SUCCESS('Root user created successfully!'))

    def create_root_user(self):
        """Create root superuser"""
        if not User.objects.filter(username='root').exists():
            root_user = User.objects.create_superuser(
                username='root',
                email='root@panlyr.com',
                password='root123',
                phone_number='+1234567890',
                address='System Address',
                city='System City', 
                country='System Country',
                _is_active=True
            )
            # Agregar al grupo Admin si existe
            try:
                admin_group = Group.objects.get(name='Admin')
                root_user.groups.add(admin_group)
            except Group.DoesNotExist:
                self.stdout.write(self.style.WARNING('Admin group not found, root user created without group'))
            
            self.stdout.write(self.style.SUCCESS('Root user created (username: root, password: root123)'))
        else:
            self.stdout.write(self.style.WARNING('Root user already exists'))