# URL de app Core
from django.contrib import admin
from django.urls import path, include
from core.views import *
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', render_home, name='home'),
    
    #CRUD DE PRODUCTOS
    path('products/', ProductListView.as_view(), name='product-index'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    
    # CATÁLOGO PÚBLICO
    path('catalogo/', views.catalogo_view, name='catalogo'),
     

    # CARRITO DE COMPRAS (CBV)
    path('cart/', CartView.as_view(), name='cart_view'),
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/update/<int:item_id>/', UpdateCartItemView.as_view(), name='update_cart_item'),
    path('cart/remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),

    # PEDIDOS (CBV)
    path('pedido/', OrderCreateView.as_view(), name='realizar_pedido'),
    path('mis-pedidos/', UserOrdersView.as_view(), name='mis_pedidos'),
    path('pedido/<int:order_id>/', OrderDetailView.as_view(), name='detalle_pedido'),
    path('pedido/<int:order_id>/subir-comprobante/', UploadReceiptView.as_view(), name='subir_comprobante'),


    # papelera para borrado suaves panel django... 
    path('products/trash/', ProductTrashView.as_view(), name='product_trash'), #Trabajar en otro momento
    
    #Panel de administación principal
    path('dashboard/', views.dashboard, name='dashboard'),

    #VISTA DE PEDIDOS REALIZADOS desde el panel dashboard
    path("pedidos/", DashboardOrdersListView.as_view(), name="dashboard-orders"),
    path("pedidos/<int:pk>/", DashboardOrderDetailView.as_view(), name="dashboard-order-detail"),
    
]