from django.urls import path
from . import views

urlpatterns = [
    path('products/upload', views.upload_product, name='upload_product'),
    path('list_products', views.list_products, name='list_products'),
    path('get_product/<str:product_id>', views.get_product, name='get_product'),
    path('update_product/<str:product_id>', views.update_product, name='update_product'),
    path('delete_product/<str:product_id>', views.delete_product, name='delete_product'),
    path('upload_csv', views.upload_csv, name='upload_csv'),
]