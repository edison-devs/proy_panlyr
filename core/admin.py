# core/admin.py
from django.contrib import admin
# Importa todos los modelos que administra esta app
from .models import (
    Category, PaymentMethod, CartStatus, OrderType, DeliveryStatus,
    OutputReason, Product, Cart, Payment, Delivery, Order, Input, Output
)

# Mixins para borrado suave y filtro visual
from abcstracts.mixin import SoftDeleteAdminMixin, DeletedAtFilterMixin

# -------------------------
# ModelAdmin para modelos sin SoftDeleteMixin
# -------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista del admin
    list_display = ("id", "name", "description")
    search_fields = ("name", "description")
    ordering = ("name",)
    list_per_page = 2


# -------------------------
# ModelAdmin para modelos con SoftDeleteMixin
# Usamos SoftDeleteAdminMixin para añadir acciones:
#  - action_soft_delete, action_hard_delete, action_restore
# y el filtro DeletedAtFilterMixin para ver "Borrados / No borrados"
# -------------------------
@admin.register(PaymentMethod)
class PaymentMethodAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = ("id", "name", "description", "created_at", "updated_at", "deleted_at")
    search_fields = ("name",)
    ordering = ("name",)
    # Añadimos el filtro de borrado suave desde el mixin
    list_filter = SoftDeleteAdminMixin.list_filter
    readonly_fields = ("created_at", "updated_at", "deleted_at")
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


# -------------------------
# Product usa SoftDeleteMixin: aplicamos el mixin en el admin
# - mostramos deleted_at en la lista
# - protegemos created_at/updated_at/deleted_at como readonly
# - filtramos por categoría y por estado de borrado
# -------------------------
@admin.register(Product)
class ProductAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = ("id", "name", "category", "price", "stock", "created_at", "updated_at", "deleted_at")
    list_display_links = ("name",)
    search_fields = ("name", "category__name", "description")
    # list_filter combinado: primero el filtro del mixin, luego filtros propios
    list_filter = SoftDeleteAdminMixin.list_filter + ["category"]
    ordering = ("-created_at",)
    list_editable = ("price", "stock")
    readonly_fields = ("created_at", "updated_at", "deleted_at", "stock")
    list_per_page = 2

    # Mostrar por defecto solo los no eliminados en la lista del admin
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(deleted_at__isnull=True)


# -------------------------
# Cart puede necesitar borrado suave si lo marcaste en el modelo
# -------------------------
@admin.register(Cart)
class CartAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = ("id", "status", "quantity", "price", "deleted_at")
    list_filter = SoftDeleteAdminMixin.list_filter + ["status"]
    ordering = ("-id",)
    readonly_fields = ("deleted_at",)
    list_per_page = 2

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(deleted_at__isnull=True)


# -------------------------
# Admins para otros modelos de negocio que usan SoftDeleteMixin
# Repite el patrón: heredar SoftDeleteAdminMixin, añadir deleted_at en list_display,
# poner readonly_fields con created_at/updated_at/deleted_at y filtrar por deleted_at en get_queryset
# -------------------------
@admin.register(Payment)
class PaymentAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = ("id", "method", "amount", "created_at", "updated_at", "deleted_at")
    search_fields = ("method__name",)
    list_filter = SoftDeleteAdminMixin.list_filter
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    list_per_page = 2

    def get_queryset(self, request):
        return super().get_queryset(request).filter(deleted_at__isnull=True)


@admin.register(Delivery)
class DeliveryAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = ("id", "user", "secondary_address", "created_at", "updated_at", "deleted_at")
    search_fields = ("user__username", "secondary_address")
    list_filter = SoftDeleteAdminMixin.list_filter
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    list_per_page = 2

    def get_queryset(self, request):
        return super().get_queryset(request).filter(deleted_at__isnull=True)


@admin.register(Order)
class OrderAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = ("id", "user", "cart", "order_type", "payment_method", "delivery", "created_at", "deleted_at")
    search_fields = ("user__username", "order_type__name")
    list_filter = SoftDeleteAdminMixin.list_filter
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    list_per_page = 2

    def get_queryset(self, request):
        return super().get_queryset(request).filter(deleted_at__isnull=True)


@admin.register(Input)
class InputAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = ("id", "product", "quantity", "created_at", "updated_at", "deleted_at")
    search_fields = ("product__name",)
    list_filter = SoftDeleteAdminMixin.list_filter
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    list_per_page = 2

    def get_queryset(self, request):
        return super().get_queryset(request).filter(deleted_at__isnull=True)


@admin.register(Output)
class OutputAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = ("id", "product", "order", "reason", "quantity", "created_at", "deleted_at")
    search_fields = ("product__name", "reason__name")
    list_filter = SoftDeleteAdminMixin.list_filter
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    list_per_page = 2

    def get_queryset(self, request):
        return super().get_queryset(request).filter(deleted_at__isnull=True)


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
