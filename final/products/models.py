from django.conf import settings
from django.db import models
from django.urls import reverse

from users.models import Address


# Create your models here.

class Product(models.Model):
    """
    product model
    """
    name = models.CharField(max_length=127, blank=False, null=False)
    description = models.TextField()
    price_no_vat = models.FloatField(null=False)
    vat = models.IntegerField(null=False, default=23)
    gtin = models.CharField(unique=True, max_length=63)
    add_date = models.DateField(auto_now_add=True)
    mod_date = models.DateField(auto_now=True)
    amount = models.IntegerField(null=False)
    category = models.ManyToManyField(to='Category')
    image = models.ImageField()

    @property
    def price_vat(self):
        """
        calculates price with vat
        """
        return self.price_no_vat * (1 + (self.vat / 100))

    @property
    def average_rating(self):
        """
        calculates average rating
        """
        result = 0
        ratings = Rating.objects.filter(product=self.id)
        ratings_count = Rating.objects.filter(product=self.id).count()
        for rating in ratings:
            result += rating.score
        result /= ratings_count
        return result

    def __str__(self):
        """
        overrides default name of objects
        """
        return self.name


class OrderItem(models.Model):
    """
    takes products and relates it to an order. it's necessary because you need to add quantity of ordered product
    """
    item = models.ForeignKey(to='Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        """
        overrides default name of objects
        """
        return f'{self.item.name}'


class Order(models.Model):
    """
    specifies order
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ManyToManyField(to='OrderItem')
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now=True)
    # ordered = models.BooleanField(default=False)
    address = models.ForeignKey(to=Address, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def ordered(self):
        """
        returns boolean value specifing if order is closed or not
        """
        if self.address is not None:
            return True
        else:
            return False

    @property
    def total(self):
        """
        calculates total to be paid
        """
        total_to_pay = 0
        order = Order.objects.get(pk=self.id)
        for item in order.item.all():
            product = Product.objects.get(pk=item.item.pk)
            subprice = product.price_vat * item.quantity
            total_to_pay += subprice
        return total_to_pay

    def get_absolute_url(self):
        """
        returns absolute url for card view"""
        return reverse('card')


class Rating(models.Model):
    """
    not implemented yet. allows users to rate products
    """
    score = models.IntegerField()
    description = models.TextField()
    add_date = models.DateField(auto_now_add=True)
    mod_date = models.DateField(auto_now=True)
    product = models.ForeignKey(to='Product', on_delete=models.CASCADE)

    # author = None

    def __str__(self):
        """
        overrides default name of objects
        """
        return f'{self.product} score: {self.score}'


class Category(models.Model):
    """
    categorizes the products. has a foregin key to itself for subcategories
    """
    name = models.CharField(max_length=64)
    description = models.TextField()
    parent_category = models.ForeignKey(to='Category', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        """
        overrides default name of objects
        """
        return self.name
