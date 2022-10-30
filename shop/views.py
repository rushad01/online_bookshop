from django.shortcuts import render
from .models import Product
# Create your views here.


def home(request):
    books = Product.objects.all()
    data = {'books': books}
    return render(request, 'profiles/home.html', data)
