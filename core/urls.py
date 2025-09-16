# URL de app Panlyr
from django.contrib import admin
from django.urls import path, include
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', render_home, name='home'),
    path('home1', render_home1, name='home1'),
]