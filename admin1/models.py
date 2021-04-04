from django.db import models


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