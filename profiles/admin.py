from django.contrib import admin

# Register your models here.
from .models import Profile, Order, OrderItem, ShippingAddress

admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
