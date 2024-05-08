from django.db import models
from app.shops.models import Shop

class Goods(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category_id = models.CharField(max_length=50)
    product_link = models.TextField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)  # 外键关联到 Shop 模型
    match_tag = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)  # auto_now_add 用于记录创建时间
    updated_at = models.DateTimeField(auto_now=True)  # auto_now 用于记录更新时间

    def __str__(self):
        return self.title