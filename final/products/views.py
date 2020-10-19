from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.models import User


from .filters import ProductFilter
from .forms import AddAddressForm
from .models import Product, Category, OrderItem, Order


# Create your views here.


class ShopView(ListView):
    """
    shows list of all products, both available and out of stock.
    """
    model = Product
    template_name = 'shop.html'
    paginate_by = 10


class CategoriesView(ListView):
    """
    upper menu in /shop/ address to select category.
    """
    model = Category
    template_name = 'categories.html'


class ProductDetailsView(DetailView):
    """
    shows details of product
    """
    model = Product
    template_name = 'product_details.html'


class ProductFilterView(View):
    """
    filters products by almost any field
    """
    def get(self, request):
        """
        displays the filter form and results.
        """
        f = ProductFilter(request.GET, queryset=Product.objects.all())
        return render(request, 'product_filter.html', {'filter': f})


class AddToCardView(LoginRequiredMixin, View):
    """
    view with no template. makes logic of adding a product to card and redirects to detail of desired product.
    """
    def post(self, request):
        """
        adds item to card or increases the number of ordered item. redirects to detail view of item
        """
        item = get_object_or_404(Product, pk=request.POST.__getitem__('product'))
        if item.amount < int(request.POST.__getitem__('quantity')):
            return redirect(f"/products/{request.POST.__getitem__('product')}/details")
        else:
            item.amount -= int(request.POST.__getitem__('quantity'))
            item.save()
        order_item = OrderItem.objects.create(item=item)
        order_item.quantity = int(request.POST.__getitem__('quantity'))
        print(order_item.quantity)
        order_qs = Order.objects.filter(user=request.user, address=None)
        if order_qs.exists():
            order = order_qs[0]
            try:
                edited_item = order.item.get(item_id=item.pk)
                edited_item.quantity += int(order_item.quantity)
                edited_item.save()
            except ObjectDoesNotExist:
                order.item.add(order_item)
                order_item.save()
                order.save()
        else:
            order = Order.objects.create(user_id=request.user.pk)
            order_item.save()
            order.item.add(order_item)
            order.save()
        return redirect(f"/products/{request.POST.__getitem__('product')}/details")


class CardView(LoginRequiredMixin, ListView):
    """
    shows all orders not shipped yet
    """
    model = Order
    template_name = 'card.html'
    paginate_by = 5

    def get_queryset(self):
        """
        filters out orders that doesn't belong to logged user
        """
        user = User.objects.get(pk=self.request.user.pk)
        return Order.objects.filter(user=user)


class AddAddressToOrderView(LoginRequiredMixin, UpdateView):
    """
    adds address to order what means closing the order and shipping it.
    """
    model = Order
    # queryset = Order.objects.filter(user_id=1)
    # fields = ['address', ]
    form_class = AddAddressForm
    template_name = 'add_address_to_order.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     print(context)
    #     return context
    #
    # def get_queryset(self):
    #     return None
