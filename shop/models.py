from django.db import models

# Create your models here.


class Product(models.Model):
    product_name = models.CharField(blank=True, max_length=255)
    price = models.FloatField(blank=True, null=True, default=1)
    digital = models.BooleanField(default=False, null=True, blank=False)
    genres = models.CharField(max_length=70)
    quantity = models.IntegerField(blank=False, default=1)
    product_pic = models.ImageField(default='default.jpg', upload_to='product')

    def __str__(self):
        return str(self.product_name)
