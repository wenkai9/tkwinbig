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


class Goods(models.Model):
    id = models.AutoField(primary_key=True)
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
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tk_goods'
