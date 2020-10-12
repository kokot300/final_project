from django_filters import FilterSet, ModelChoiceFilter

from .models import Product, Category


class ProductFilter(FilterSet):
    category = ModelChoiceFilter(queryset=Category.objects.all())
    class Meta:
        model = Product
        fields = {
            'name': ['icontains'],
            'description': ['icontains'],
            'price_no_vat': ['lte', 'gte'],
            'amount': ['lte', 'gte'],
            # 'category__name': ['exact'],
        }
