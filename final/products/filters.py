from django_filters import FilterSet, ModelChoiceFilter

from .models import Product, Category


class ProductFilter(FilterSet):
    """
    generates filterset for product model
    """
    category = ModelChoiceFilter(queryset=Category.objects.all())

    class Meta:
        """
        specifies model to be used and fields.
        """
        model = Product
        fields = {
            'name': ['icontains'],
            'description': ['icontains'],
            'price_no_vat': ['lte', 'gte'],
            'amount': ['lte', 'gte'],
            # 'category__name': ['exact'],
        }
