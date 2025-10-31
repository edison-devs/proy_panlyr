# abstract/groups.py
from django.contrib.auth.models import Group
from django import template

register = template.Library()

class GroupManager:
    GROUPS = {
        'admin': 'admin',
        'employed': 'employed', 
        'viewer': 'viewer'
    }
    
    @classmethod
    def user_has_group(cls, user, group_name):
        """Verifica si el usuario pertenece a un grupo específico"""
        if not user or not user.is_authenticated:
            return False
        return user.groups.filter(name=group_name).exists()
    
    @classmethod
    def user_has_any_group(cls, user, group_names):
        """Verifica si el usuario pertenece a alguno de los grupos"""
        if not user or not user.is_authenticated:
            return False
        
        if isinstance(group_names, str):
            group_names = [g.strip() for g in group_names.split(',')]
        
        return user.groups.filter(name__in=group_names).exists()
    
    @classmethod
    def get_user_groups(cls, user):
        """Obtiene la lista de grupos del usuario"""
        if not user or not user.is_authenticated:
            return []
        return list(user.groups.values_list('name', flat=True))

# Filtros personalizados para templates
@register.filter(name='has_group')
def has_group(user, group_name):
    return GroupManager.user_has_group(user, group_name)

@register.filter(name='has_any_group')
def has_any_group(user, group_names):
    return GroupManager.user_has_any_group(user, group_names)

@register.filter(name='get_groups')
def get_groups(user):
    return GroupManager.get_user_groups(user)