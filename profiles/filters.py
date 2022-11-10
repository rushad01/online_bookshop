import django_filters

from shop.models import Product


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {'genres': ['exact'],
                  'digital': ['exact'],
                  'product_name': ['icontains'],
                  'author_name': ['icontains']}
