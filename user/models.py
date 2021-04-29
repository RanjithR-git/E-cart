from django.db import models
from django.contrib.auth.models import User, auth
from admin1.models import product
from datetime import date
# Create your models here.

class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.BigIntegerField()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cart_product = models.ForeignKey(product, on_delete = models.CASCADE, null = True)  
    quantity = models.IntegerField(null=True, blank=True)

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    address = models.TextField(max_length=500)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.IntegerField()

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ForeignKey(product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    totalprice = models.IntegerField(null=True, blank=True)
    tid = models.CharField(max_length=200, null=True, blank=True)
    tdate = models.DateField(null=True, blank=True)
    payment_status = models.CharField(max_length=50, null=True, blank=True)
    order_status = models.CharField(max_length=50, null=True, blank=True)
    payment_mode = models.CharField(max_length=50, null=True, blank=True)

class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profilepic = models.ImageField(null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)

    @property
    def ImageURL(self):
        try:
            url = self.profilepic.url
        except:
            url = ''
        return url