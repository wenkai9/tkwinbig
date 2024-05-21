from django.db import models
from app.goods.models import Goods
from app.shops.models import Shop
from app.users.models import User


class Task(models.Model):
    TASK_STATUS_CHOICES = (
        ('1', '未启动'),
        ('2', '正在进行'),
        ('3', '已完成'),
    )
    taskId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    product = models.ForeignKey(Goods, on_delete=models.CASCADE)
    region = models.CharField(max_length=20)
    status = models.CharField(max_length=1, choices=TASK_STATUS_CHOICES,default='1')
    match_quantity = models.IntegerField(null=True)
    willing_quantity = models.IntegerField(null=True)
    send_quantity = models.IntegerField(null=True)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.taskId)

    class Meta:
        db_table = 'tk_tasks'
