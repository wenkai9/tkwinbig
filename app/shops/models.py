from django.db import models

from app.users.models import User


# Create your models here.


class Shop(models.Model):
    shopId = models.CharField(max_length=255, primary_key=True)
    shop_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shop_name

    class Meta:
        db_table = 'tk_shops'
