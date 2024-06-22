from django.db import models

# Create your models here.

class RegisterUser(models.Model):
    res_mail = models.CharField(max_length=100, blank=True)
    res_pwd = models.CharField(max_length=100, blank=True)