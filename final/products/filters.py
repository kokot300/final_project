from django_filters import FilterSet

from .models import Product


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['icontains'],
            'description': ['icontains'],
            'price_no_vat': ['lte', 'gte'],
            'amount': ['lte', 'gte'],
            'category': [],
        }
