from django.db import models
from django.contrib.auth.models import User

from shop.models import Product


# Create your models here.

# Profile Table for user for facilitating extended features

# It has one to one relationship with user table


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True)
    profile_pic = models.ImageField(default='default.png', upload_to='profile')

    def __str__(self):
        return f'{self.user.username} Profile'


# model for cart
class Order(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False, null=True)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.profile} Order no {self.id}'

    @ property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @ property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True

            return shipping


# Item detail of Cart
class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @ property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return str(self.product.product_name)


# Delivery Address
class ShippingAddress(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.address)

# For recommendation analysis


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=100, default='Untitled')
    rating = models.CharField(max_length=70)
    review = models.CharField(max_length=250)
    rated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} profile {self.product.product_name} rating'
