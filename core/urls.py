# URL de app Panlyr
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
    
      # otras rutas existentes...
    path('pedido/', views.realizar_pedido, name='realizar_pedido'), #Aun no tiene asignada una template
      
      # papelera para borrado suaves panel django... 
    path('products/trash/', ProductTrashView.as_view(), name='product_trash'), #Trabajar en otro momento
    
    
    #Panel de administación principal
    path('dashboard/', views.dashboard, name='dashboard'),
]