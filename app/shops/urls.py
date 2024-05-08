from django.urls import path
from . import views

urlpatterns = [
    # path('home/', views.home, name='home'),
    path('create_shop/', views.create_shop, name='create_shop'),
    path('view_shop/<int:shopId>/', views.view_shop, name='view_shop'),
    path('update_shop/<int:shopId>/', views.update_shop, name='update_shop'),
    path('delete_shop/<int:shopId>/', views.delete_shop, name='delete_shop'),
]
