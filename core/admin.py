from django.contrib import admin
from .models import (
    Category, PaymentMethod, CartStatus, OrderType, DeliveryStatus,
    OutputReason, Product, Cart
)
from abcstracts.mixin import SoftDeleteAdminMixin

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name", "description")
    ordering = ("name",)
    list_per_page = 2


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "created_at")
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 2


@admin.register(CartStatus)
class CartStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)
    list_per_page = 2


@admin.register(OrderType)
class OrderTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)
    list_per_page = 2


@admin.register(DeliveryStatus)
class DeliveryStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)
    list_per_page = 2


@admin.register(OutputReason)
class OutputReasonAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)
    list_per_page = 2


@admin.register(Product)
class ProductAdmin(SoftDeleteAdminMixin, admin.ModelAdmin): # ← hereda del mixin, no de ModelAdmin dos veces
    list_display = ("id", "name", "category", "price", "stock", "created_at", "updated_at", "deleted_at")
    list_display_links = ("name",)
    search_fields = ("name", "category__name")
    list_filter = SoftDeleteAdminMixin.list_filter + ["category"]
    ordering = ("-created_at",)
    list_editable = ("price", "stock")
    list_per_page = 2
    readonly_fields = ['created_at', 'updated_at', 'deleted_at', 'stock']



@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "quantity", "price")
    list_filter = ("status",)
    ordering = ("-id",)
    list_per_page = 2

# Registra el modelo User en el admin usando esta clase personalizada
# @admin.register(User)
# class UserAdmin(SoftDeleteAdmin, BaseUserAdmin):
#     # Define el modelo que esta clase administra
#     model = User

#     # Lista de acciones disponibles en el menú "Acción" del admin
#     actions = ['action_soft_delete', 'action_hard_delete', 'action_restore']

#     # Campos que se mostrarán como columnas en la tabla del admin
#     list_display = [
#         'username', 'email', 'is_active', 'is_staff', 'is_superuser',
#         'created_at', 'updated_at', 'deleted_at'
#     ]

#     # Filtros laterales en el panel del admin (incluye el filtro de borrado suave)
#     list_filter = SoftDeleteAdmin.list_filter + ['is_active', 'is_staff', 'is_superuser']

#     # Campos por los que se puede buscar en el admin
#     search_fields = ['username', 'email']

#     # Ordenamiento por defecto en la tabla del admin
#     ordering = ['username']

#     # Campos que se muestran como solo lectura en el formulario de edición
#     readonly_fields = ['created_at', 'updated_at', 'deleted_at']

#     # Organización de campos en el formulario de edición de usuario
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),  # Sección básica
#         ('Información personal', {'fields': ('email', 'phone_number', 'address', 'city', 'country')}),  # Datos personales
#         ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),  # Roles y permisos
#         ('Fechas', {'fields': ('last_login', 'created_at', 'updated_at', 'deleted_at')}),  # Trazabilidad temporal
#     )

#     # Organización de campos en el formulario de creación de usuario
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),  # Estilo visual del formulario
#             'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
#         }),
#     )
