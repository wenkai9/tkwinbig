from django.urls import path
from . import views

urlpatterns = [
    # path('home/', views.home, name='home'),
    # 创建商铺
    path('create_shop/', views.create_shop, name='create_shop'),
    # 商铺列表
    path('list_shops/', views.list_shops, name='list_shops'),
    # 商铺详情
    path('view_shop/<int:shopId>/', views.view_shop, name='view_shop'),
    # 商铺更新
    path('update_shop/<int:shopId>/', views.update_shop, name='update_shop'),
    # 商铺删除
    path('delete_shop/<int:shopId>/', views.delete_shop, name='delete_shop'),
]
