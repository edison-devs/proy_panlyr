# URL de app Core
from django.contrib import admin
from django.urls import path
from core import views
from core.views import *

urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),

    # Home
    path('', render_home, name='home'),

    # -----------------------------
    # CRUD PRODUCTOS (PANEL)
    # -----------------------------
    path('products/', ProductListView.as_view(), name='product-index'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),

    # Papelera (soft delete)
    path('products/trash/', ProductTrashView.as_view(), name='product_trash'), #Para trabajar mas adelante

    # -----------------------------
    # CATÁLOGO PÚBLICO
    # -----------------------------
    path('catalogo/', views.catalogo_view, name='catalogo'),

    # -----------------------------
    # CARRITO (CBV)
    # -----------------------------
    path('cart/', CartView.as_view(), name='cart_view'),
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/update/<int:item_id>/', UpdateCartItemView.as_view(), name='update_cart_item'),
    path('cart/remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),

    # -----------------------------
    # PEDIDOS CLIENTE
    # -----------------------------
    path('pedido/', OrderCreateView.as_view(), name='realizar_pedido'),
    path('mis-pedidos/', UserOrdersView.as_view(), name='mis_pedidos'),
    path('pedido/<int:order_id>/', OrderDetailView.as_view(), name='detalle_pedido'),
    path('pedido/<int:order_id>/subir-comprobante/', UploadReceiptView.as_view(), name='subir_comprobante'),

    # -----------------------------
    # DASHBOARD
    # -----------------------------
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/pedidos/', DashboardOrdersListView.as_view(), name='dashboard-orders'),
    path('dashboard/pedidos/<int:pk>/', DashboardOrderDetailView.as_view(), name='dashboard-order-detail'),
]