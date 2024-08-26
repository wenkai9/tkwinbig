from django.db import models
from app.shops.models import Shop


class base_category1(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'base_category1'


class base_category2(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    category1 = models.ForeignKey(base_category1, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'base_category2'


class RaidsysRule(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    requirement = models.TextField()
    commission = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    shop_info = models.CharField(max_length=100, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tk_raidsys_rule'


class Goods(models.Model):
    GOODS_STATUS_CHOICES = (
        (False, '未建联'),
        (True, '已经建联'),
    )
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    hasFreeSample = models.BooleanField(default=False)
    commissionRate = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    CooperationFee = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    base_category2 = models.ForeignKey(base_category2, on_delete=models.CASCADE)
    product_link = models.TextField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    match_tag = models.CharField(max_length=100)
    product_status = models.BooleanField(choices=GOODS_STATUS_CHOICES, default=False)
    raidsysrule = models.ForeignKey(RaidsysRule, on_delete=models.CASCADE, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tk_goods'

# 商家登录后去设置多个建联规则，上传物品时商家自行去选择建联规则
