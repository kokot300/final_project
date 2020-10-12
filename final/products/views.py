from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .filters import ProductFilter
from .models import Product, Category, OrderItem, Order


# Create your views here.


class ShopView(ListView):
    model = Product
    template_name = 'shop.html'
    paginate_by = 10


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


class AddToCardView(LoginRequiredMixin, View):
    def post(self, request):
        print(request.POST.__getitem__('product'))
        item = get_object_or_404(Product, pk=request.POST.__getitem__('product'))
        if item.amount < int(request.POST.__getitem__('quantity')):
            return redirect(f"/products/{request.POST.__getitem__('product')}/details")
        else:
            item.amount -= int(request.POST.__getitem__('quantity'))
            item.save()
        order_item = OrderItem.objects.create(item=item)
        order_item.quantity = request.POST.__getitem__('quantity')
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.item.filter(item__pk=item.pk).exists():
                order_item.quantity += request.POST.__getitem__('quantity')
                order.save()
            else:
                print(order.item.all())
                order.item.add(order_item)
                order.save()
        else:
            order = Order.objects.create(user_id=request.user.pk)
            order.item.add(order_item)
            order.save()

        order_item.save()

        return redirect(f"/products/{request.POST.__getitem__('product')}/details")


class CardView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'card.html'
    paginate_by = 5
