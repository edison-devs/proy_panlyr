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

    def value(self):
        return super().value()

    def queryset(self, request, queryset):
        if self.value() == 'no':
            return queryset.filter(deleted_at__isnull=True)
        elif self.value() == 'yes':
            return queryset.filter(deleted_at__isnull=False)
        return queryset  # Sin filtro = todos


#----------------------------------------------------------------------------------------------------

class SoftDeleteActionsAdminMixin():
    actions = ['action_soft_delete', 'action_hard_delete', 'action_restore']

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop('delete_selected', None)

        opts = self.model._meta
        perm_codename = f"{opts.app_label}.delete_{opts.model_name}"

        if not (request.user.is_superuser or request.user.has_perm(perm_codename)):
            for action_name in ['action_soft_delete', 'action_hard_delete', 'action_restore']:
                actions.pop(action_name, None)

        return actions


    def action_soft_delete(self, request, queryset):
        updated = 0
        for obj in queryset:
            if hasattr(obj, 'deleted_at') and not obj.deleted_at:
                obj.soft_delete()
                updated += 1
        self.message_user(request, f"{updated} objeto(s) borrado(s) suavemente.")
    action_soft_delete.short_description = "Borrado suave de seleccionados"

    def action_hard_delete(self, request, queryset):
        deleted = 0
        for obj in queryset:
            obj.delete()
            deleted += 1
        self.message_user(request, f"{deleted} objeto(s) borrado(s) definitivamente.")
    action_hard_delete.short_description = "Borrado definitivo de seleccionados"

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
