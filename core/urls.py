# URL de app Panlyr
from django.contrib import admin
from django.urls import path, include
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', render_home, name='home'),
    path('home1', render_home1, name='home1'),
    path('products/', ProductListView.as_view(), name='product_catalog'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/trash/', ProductTrashView.as_view(), name='product_trash'), #Trabajar en otro momento

]