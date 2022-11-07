from django.shortcuts import render
from .models import Product
from profiles.models import Order, OrderItem
from profiles.filters import ProductFilter
# Create your views here.


def home(request):
    books = Product.objects.all()
    books_filter = ProductFilter(request.GET, queryset=books)
    if request.user.is_authenticated:
        customer = request.user.profile
        # tuple unpacking
        order, created = Order.objects.get_or_create(
            profile=customer, completed=False)
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    data = {'books': books, 'cartItems': cartItems,
            'books_filter': books_filter}

    return render(request, 'profiles/home.html', data)
