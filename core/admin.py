from django.contrib import admin
from .models import (
    Category, PaymentMethod, CartStatus, OrderType, DeliveryStatus,
    OutputReason, Product, Cart
)


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
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price", "stock", "created_at", "updated_at")
    list_display_links = ("id", "name")
    search_fields = ("name", "category__name")
    list_filter = ("category",)
    ordering = ("-created_at",)
    list_editable = ("price", "stock")  # edición rápida
    list_per_page = 2


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "quantity", "price")
    list_filter = ("status",)
    ordering = ("-id",)
    list_per_page = 2