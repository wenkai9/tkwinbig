from django.urls import path
from . import views

urlpatterns = [
    path('user/register', views.user_register, name='register'),
    path('user/login', views.user_login, name='user_login'),
    path('user/user_profile', views.user_profile, name='user_profile'),
    path('user/change_password', views.change_password, name='change_password'),
    path('user/logout', views.user_logout, name='user_logout'),
]