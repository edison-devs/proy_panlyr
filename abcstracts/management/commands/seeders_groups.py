# core/management/commands/seed_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Create default groups (admin, employee, viewer)'

    def handle(self, *args, **options):
        self.stdout.write('Creating default groups...')
        
        # Crear grupos
        admin_group = self.create_admin_group()
        employee_group = self.create_employee_group()
        viewer_group = self.create_viewer_group()
        
        self.stdout.write(self.style.SUCCESS('Default groups created successfully!'))

    def create_admin_group(self):
        """Create Admin group with all permissions"""
        group, created = Group.objects.get_or_create(name='Admin')
        if created:
            all_permissions = Permission.objects.all()
            group.permissions.set(all_permissions)
            self.stdout.write(self.style.SUCCESS('Admin group created with all permissions'))
        else:
            self.stdout.write(self.style.WARNING('Admin group already exists'))
        return group

    def create_employee_group(self):
        """Create Employee group with limited permissions"""
        group, created = Group.objects.get_or_create(name='Employee')
        if created:
            permissions = Permission.objects.filter(
                codename__in=[
                    'add_product', 'change_product', 'view_product',
                    'add_category', 'change_category', 'view_category', 
                    'add_order', 'change_order', 'view_order',
                    'add_cart', 'change_cart', 'view_cart',
                    'add_delivery', 'change_delivery', 'view_delivery',
                    'add_payment', 'change_payment', 'view_payment',
                    'add_input', 'change_input', 'view_input',
                    'add_output', 'change_output', 'view_output',
                    'soft_delete_product', 'restore_product',
                    'soft_delete_order', 'restore_order',
                    'soft_delete_cart', 'restore_cart',
                ]
            )
            group.permissions.set(permissions)
            self.stdout.write(self.style.SUCCESS('Employee group created with operational permissions'))
        else:
            self.stdout.write(self.style.WARNING('Employee group already exists'))
        return group

    def create_viewer_group(self):
        """Create Viewer group with read-only permissions"""
        group, created = Group.objects.get_or_create(name='Viewer')
        if created:
            permissions = Permission.objects.filter(codename__startswith='view_')
            group.permissions.set(permissions)
            self.stdout.write(self.style.SUCCESS('Viewer group created with view-only permissions'))
        else:
            self.stdout.write(self.style.WARNING('Viewer group already exists'))
        return group