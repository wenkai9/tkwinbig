from django.db import models

from app.users.models import User


# Create your models here.


# 订单表
class order_indo(models.Model):
    order_id = models.CharField(max_length=100)
    total_amount = models.IntegerField()
    order_status = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_indo')
    payment_way = models.CharField(max_length=100)
    order_comment = models.CharField(max_length=100)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_id

    class Meta:
        verbose_name_plural = "Order Indo"


# 订单状态流水表
class order_status_log(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(order_indo, on_delete=models.CASCADE, related_name='order_status_log')
    order_status = models.CharField(max_length=100)
    operate_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_status

    class Meta:
        verbose_name_plural = "Order Status Log"


# 支付表
class payment_info(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(order_indo, on_delete=models.CASCADE, related_name='payment_info')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_info')
    payment_way = models.CharField(max_length=100)
    total_amount = models.IntegerField()
    payment_status = models.CharField(max_length=100)
    createAt = models.DateTimeField(auto_now_add=True)
    callback = models.CharField(max_length=100)
    callback_code = models.CharField(max_length=100)

    def __str__(self):
        return self.payment_status

    class Meta:
        verbose_name_plural = "Payment Info"


# 订单明细表
class order_detail(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(order_indo, on_delete=models.CASCADE, related_name='order_detail')
    order_price = models.IntegerField()
    num = models.IntegerField()
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order.order_id

    class Meta:
        verbose_name_plural = "Order Detail"
