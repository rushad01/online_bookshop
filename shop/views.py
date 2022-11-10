from django.shortcuts import render
from .models import Product
from profiles.models import Order, OrderItem
from profiles.filters import ProductFilter
from django.core.paginator import Paginator
# Create your views here.


def home(request):
    books = Product.objects.all()
    books_filter = ProductFilter(request.GET, queryset=books)
    paginator = Paginator(books_filter.qs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
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

    data = {'cartItems': cartItems,
            'books_filter': books_filter, 'page_obj': page_obj}

    return render(request, 'profiles/home.html', data)
