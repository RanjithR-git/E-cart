from django.db import models
from django.contrib.auth.models import User, auth
from datetime import date
class Categories(models.Model):
    category =models.CharField(max_length=50)

    
# # # Create your models here.
class product(models.Model):
    product_name =models.CharField(max_length=50)
    category =models.ForeignKey(Categories, on_delete=models.CASCADE)    
    price = models.IntegerField()
    desc =models.CharField(max_length=300)
    image =models.ImageField(upload_to='img') 
    quantity=models.IntegerField()

    @property
    def ImageURL(self):
        try:
            url= self.image.url
        except:
            url=''
        return url

class Coupons(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    coupen_name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    percent = models.IntegerField()
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    used = models.BooleanField(default=False)
    live = models.BooleanField(default=False)

    @property
    def is_started(self):
        return date.today() >= self.start


    @property
    def is_valid(self):
        return date.today() > self.end

class Offer(models.Model):
    category = models.OneToOneField(Categories,on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    discount = models.DecimalField(max_digits=20,decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    start = models.BooleanField(default=False)

    @property
    def is_valid(self):
        return date.today() > self.end_date
    
    @property
    def is_started(self):
        return date.today() >= self.start_date