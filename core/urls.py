# URL de app core
from django.urls import path, include
from core.views import *



urlpatterns = [
    path('', render_home, name='home'),
    path('home1', render_home1, name='home1'),
]