from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from auth_users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Campos que se muestran en la lista
    list_display = ("id", "username", "email", "phone_number", "is_active", "is_staff", "created_at")
    list_display_links = ("id", "username")  # campos clicables
    search_fields = ("username", "email", "phone_number")
    list_filter = ("is_active", "is_staff", "is_superuser", "city", "country")
    ordering = ("-date_joined",)

    # Paginación (opcional, por defecto son 100)
    list_per_page = 2

    # Organización de los campos en el formulario de edición
    fieldsets = UserAdmin.fieldsets + (
        ("Información adicional", {"fields": ("phone_number", "address", "city", "country")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("email", "phone_number", "address", "city", "country")}),
    )