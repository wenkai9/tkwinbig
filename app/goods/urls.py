from django.urls import path
from . import views

urlpatterns = [
    # 添加商品
    path('add_products', views.add_product, name='upload_product'),
    path('add_products/<int:page>', views.add_product, name='upload_product_paged'),
    # 商品列表
    path('list_products', views.list_products, name='list_products'),
    path('list_products/<int:page>', views.list_products, name='list_products_paged'),
    # 商品详情
    path('get_product/<str:product_id>', views.get_product, name='get_product'),
    # 编辑商品
    path('update_product/<str:product_id>', views.update_product, name='update_product'),
    # 删除商品
    path('delete_product/<str:product_id>', views.delete_product, name='delete_product'),
    # 上传csv文件
    path('upload_csv', views.upload_csv, name='upload_csv'),
    # 下载excel文件
    path('download_excel', views.download_excel, name='download_excel'),
    # 获取全部类目下的商品信息
    path('all_category_products', views.list_category_products, name='all_category_products'),
    # 新增规则
    path('add_rules', views.add_rule, name='add_rules'),
    # 建联列表
    path('list_rules', views.list_rule, name='list_rules'),
    path('list_rules/<int:page>', views.list_rule, name='list_rules_paged'),
    # 删除规则
    path('delete_rule/<int:rule_id>', views.delete_rule, name='delete_rule'),
    # 编辑规则
    path('update_rule/<int:id>', views.update_rule, name='update_rule'),
]
