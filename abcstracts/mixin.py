from django.shortcuts import render

from django.contrib import admin
from django.contrib.admin import SimpleListFilter

class DeletedAtFilterMixin(SimpleListFilter):
    title = 'Estado de borrado'
    parameter_name = 'deleted'

    def lookups(self, request, model_admin):
        return (
            ('no', 'No borrados'),
            ('yes', 'Borrados'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'no':
            return queryset.filter(deleted_at__isnull=True)
        elif self.value() == 'yes':
            return queryset.filter(deleted_at__isnull=False)
        return queryset

#----------------------------------------------------------------------------------------------------

class SoftDeleteActionsAdminMixin():
    actions = ['action_soft_delete', 'action_restore']

    def get_actions(self, request):
        actions = super().get_actions(request)
        
        opts = self.model._meta
        
        # Verificar si este modelo hereda de SoftDeleteMixin (no SoftDeleteModel)
        is_softdelete_model = any(
            base.__name__ == 'SoftDeleteMixin' for base in self.model.__mro__
        )
        
        if is_softdelete_model:
            # Usar permisos específicos de soft delete
            if not (request.user.is_superuser or 
                    request.user.has_perm(f"{opts.app_label}.soft_delete_{opts.model_name}")):
                actions.pop('action_soft_delete', None)
            
            if not (request.user.is_superuser or 
                    request.user.has_perm(f"{opts.app_label}.restore_{opts.model_name}")):
                actions.pop('action_restore', None)
        else:
            # Si no es soft delete model, ocultar las acciones
            actions.pop('action_soft_delete', None)
            actions.pop('action_restore', None)

        return actions

    def action_soft_delete(self, request, queryset):
        updated = 0
        for obj in queryset:
            if hasattr(obj, 'deleted_at') and not obj.deleted_at:
                obj.soft_delete()
                updated += 1
        self.message_user(request, f"{updated} objeto(s) borrado(s) suavemente.")
    action_soft_delete.short_description = "Borrado suave de seleccionados"

    def action_restore(self, request, queryset):
        restored = 0
        for obj in queryset:
            if hasattr(obj, 'deleted_at') and obj.deleted_at:
                obj.restore()
                restored += 1
        self.message_user(request, f"{restored} objeto(s) restaurado(s).")
    action_restore.short_description = "Restaurar seleccionados"

#----------------------------------------------------------------------------------------------------

class SoftDeleteAdminMixin(SoftDeleteActionsAdminMixin):
    list_filter = [DeletedAtFilterMixin]
    
    def get_list_filter(self, request):
        list_filter = super().get_list_filter(request)
        
        opts = self.model._meta
        if not (request.user.is_superuser or 
                request.user.has_perm(f"{opts.app_label}.restore_{opts.model_name}")):
            # Si no tiene permiso de RESTORE, quitar el filtro de borrado
            if list_filter and DeletedAtFilterMixin in list_filter:
                list_filter = [f for f in list_filter if f != DeletedAtFilterMixin]
        
        return list_filter