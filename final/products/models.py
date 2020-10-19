from django.conf import settings
from django.db import models
from django.urls import reverse

from users.models import Address


# Create your models here.

class Product(models.Model):
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
        return self.price_no_vat * (1 + (self.vat / 100))

    @property
    def average_rating(self):
        result = 0
        ratings = Rating.objects.filter(product=self.id)
        ratings_count = Rating.objects.filter(product=self.id).count()
        for rating in ratings:
            result += rating.score
        result /= ratings_count
        return result

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    item = models.ForeignKey(to='Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.item.name}'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ManyToManyField(to='OrderItem')
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now=True)
    # ordered = models.BooleanField(default=False)
    address = models.ForeignKey(to=Address, on_delete=models.CASCADE, null=True, blank=True)


    @property
    def ordered(self):
        if self.address is not None:
            return True
        else:
            return False

    @property
    def total(self):
        total_to_pay = 0
        order = Order.objects.get(pk=self.id)
        for item in order.item.all():
            product = Product.objects.get(pk=item.item.pk)
            subprice = product.price_vat * item.quantity
            total_to_pay += subprice
        return total_to_pay

    def get_absolute_url(self):
        return reverse('card')


class Rating(models.Model):
    score = models.IntegerField()
    description = models.TextField()
    add_date = models.DateField(auto_now_add=True)
    mod_date = models.DateField(auto_now=True)
    product = models.ForeignKey(to='Product', on_delete=models.CASCADE)

    # author = None

    def __str__(self):
        return f'{self.product} score: {self.score}'


class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()

    # kategoria do kategorii
    parent_category = models.ForeignKey(to='Category', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
