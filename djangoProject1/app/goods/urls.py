from django.urls import path
from . import views

urlpatterns = [
    path('products/upload', views.upload_product, name='upload_product'),
    path('products/<str:product_id>', views.get_product, name='get_product'),
    path('products/<str:product_id>', views.update_product, name='update_product'),
    path('products/<str:product_id>', views.delete_product, name='delete_product'),
]