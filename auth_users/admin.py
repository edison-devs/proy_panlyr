# auth_users/admin.py
from django.contrib import admin
# Importamos BaseUserAdmin para mantener comportamiento de UserAdmin predeterminado
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from auth_users.models import User

# Mixins para borrado suave (acciones y filtro)
from abcstracts.mixin import SoftDeleteAdminMixin

# -------------------------
# Admin personalizado para User
# - Hereda SoftDeleteAdminMixin para añadir acciones de soft delete
# - Hereda BaseUserAdmin (UserAdmin original) para mantener formularios y comportamiento
# -------------------------
@admin.register(User)
class CustomUserAdmin(SoftDeleteAdminMixin, BaseUserAdmin):
    model = User

    # Si el mixin ya define las acciones, aquí las repetimos para claridad
    actions = ['action_soft_delete', 'action_hard_delete', 'action_restore']

    # Columnas que se verán en la lista de usuarios
    list_display = (
        "id", "username", "email", "phone_number",
        "is_active", "is_staff", "is_superuser",
        "created_at", "updated_at", "deleted_at"
    )
    list_display_links = ("id", "username")
    search_fields = ("username", "email", "phone_number")
    # Combinamos filtros del mixin con filtros de permisos y ubicación
    list_filter = SoftDeleteAdminMixin.list_filter + ["_is_active", "is_staff", "is_superuser", "city", "country"]
    # Orden por defecto; ajusta si quieres por fecha de creación en lugar de date_joined
    ordering = ("-date_joined",)
    readonly_fields = ("created_at", "updated_at", "deleted_at")
   
    # Paginación (opcional, por defecto son 100)
    list_per_page = 2

    # Añadimos secciones adicionales al formulario de edición (manteniendo las del BaseUserAdmin)
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Información adicional", {"fields": ("phone_number", "address", "city", "country")}),
        ("Fechas", {"fields": ("created_at", "updated_at", "deleted_at")}),
    )

    # Campos para el formulario de creación
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {"fields": ("email", "phone_number", "address", "city", "country")}),
    )

    
    # Mostrar estado legible en la lista (opcional): "Eliminado / Activo / Inactivo"
    def estado_usuario(self, obj):
        if obj.deleted_at:
            return "🗑️ Eliminado"
        elif getattr(obj, "_is_active", True):
            return "✅ Activo"
        else:
            return "⛔ Inactivo"
    estado_usuario.short_description = "Estado"
