from django.urls import path
from . import views

urlpatterns = [
    path('generate_order/', views.generate_order, name='generate_order'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('display_order/<str:order_id>/', views.display_order, name='display_order'),
]
