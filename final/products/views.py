from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from .filters import ProductFilter
from .models import Product, Category


# Create your views here.


class ShopView(ListView):
    model = Product
    template_name = 'shop.html'


class CategoriesView(ListView):
    model = Category
    template_name = 'categories.html'


class ProductDetailsView(DetailView):
    model = Product
    template_name = 'product_details.html'


class ProductFilterView(View):
    def get(self, request):
        f = ProductFilter(request.GET, queryset=Product.objects.all())
        return render(request, 'product_filter.html', {'filter': f})
