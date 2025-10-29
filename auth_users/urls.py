# URL de app auth_users
from django.urls import path
from .views import *

urlpatterns = [
    # ... URLs ...
    path('login/', UserLoginView.as_view(), name='login'),       
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name= 'logout'), 
    
]
