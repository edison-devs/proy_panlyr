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
    
    # CARRITO DE COMPRAS
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # PEDIDOS
    path('pedido/', views.realizar_pedido, name='realizar_pedido'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('pedido/<int:order_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('pedido/<int:order_id>/subir-comprobante/', views.subir_comprobante, name='subir_comprobante'),
      
      # papelera para borrado suaves panel django... 
    path('products/trash/', ProductTrashView.as_view(), name='product_trash'), #Trabajar en otro momento
    
    #Panel de administación principal
    path('dashboard/', views.dashboard, name='dashboard'),
]