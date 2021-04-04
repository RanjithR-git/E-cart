from django.db import models
from django.contrib.auth.models import User, auth
from admin1.models import *
# Create your models here.

class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.BigIntegerField()

# class Ecart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
#     product = models.ForeignKey(product, on_delete=models.CASCADE, null=True, blank=True)
#     quantity = models.IntegerField(null=True, blank=True)
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)