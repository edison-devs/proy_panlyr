# URL de app Panlyr
from django.contrib import admin
from django.urls import path, include
from core.views import *
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('panel/', panel_view, name='panel'),
    path('panel/superadmin/', superadmin_dashboard, name='superadmin_dashboard'),
	  path('panel/admin/', admin_dashboard, name='admin_dashboard'),
	  path('panel/cliente/', client_dashboard, name='client_dashboard'),
    path('', render_home, name='home'),
    path('home1', render_home1, name='home1'),
    path('products/', ProductListView.as_view(), name='product_catalog'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
      # otras rutas existentes...
    path('pedidos/', pedidos_list, name='pedidos_list'),
    path('papelera/',papelera, name='papelera'),
    path('carrito/', carrito, name='carrito'),
    path('mis-pedidos/', mis_pedidos, name='mis_pedidos'),
    path('reportes/', reportes, name='reportes'),
      # otras rutas existentes... 
    path('products/trash/', ProductTrashView.as_view(), name='product_trash'), #Trabajar en otro momento
    path('pedido/', views.realizar_pedido, name='realizar_pedido'),
    path('dashboard/', views.dashboard, name='dashboard'),
]