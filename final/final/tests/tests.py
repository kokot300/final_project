from random import randint, random

from django.contrib.auth.models import User
from django.test import TestCase
from faker import Faker

from products.models import Product, Category, OrderItem

faker = Faker('pl_PL')


class GetOnlyViewsTest(TestCase):
    """
    test simple views that support only get method
    """

    def test_get_to_root(self):
        """
        tests get method for root
        """
        response = self.client.get("/")
        assert response.status_code == 200

    def test_post_to_root(self):
        """
        tests post method for root
        """
        response = self.client.post("/")
        assert response.status_code == 405

    def test_get_to_products(self):
        """
        tests get method for /products/
        """
        response = self.client.get("/products/")
        assert response.status_code == 200

    def test_post_to_products(self):
        """
        tests post method for /products/
        """
        response = self.client.post("/products/")
        assert response.status_code == 405

    def test_get_to_about(self):
        """
        tests get method for /about/
        """
        response = self.client.get("/about/")
        assert response.status_code == 200

    def test_post_to_about(self):
        """
        tests post method for /about/
        """
        response = self.client.post("/about/")
        assert response.status_code == 405

    def test_get_to_contact(self):
        """
        tests get method for /contact/
        """
        response = self.client.get("/contact/")
        assert response.status_code == 200

    def test_post_to_contact(self):
        """
        tests post method for /contact/
        """
        response = self.client.post("/contact/")
        assert response.status_code == 405


class AddToCardTest(TestCase):
    """
    checks ability to add a product to card.
    """

    def setUp(self):
        for _ in range(5):
            name = faker.first_name()
            description = faker.last_name()
            price_no_vat = random()
            vat = 23
            gtin = faker.ean(length=13)
            amount = randint(1, 1000)
            category = Category.objects.create(name=faker.first_name(), description=faker.last_name())
            product = Product.objects.create(name=name, description=description, price_no_vat=price_no_vat, vat=vat,
                                             gtin=gtin,
                                             amount=amount)
        user = User.objects.create_user(username='kokot', password='1234')

    def test_get(self):
        """
        302 expected. View requires login and POST
        """
        response = self.client.get('/products/add_to_card/')
        assert response.status_code == 302

    def test_post(self):
        """
        302 expected. login required
        """
        response = self.client.post('/products/add_to_card/')
        assert response.status_code == 302

    def test_post_login(self):
        """
        one orderitem should be added
        """
        start_count = OrderItem.objects.count()
        user = User.objects.get(username='kokot')
        product = Product.objects.first()
        self.client.login(username=user.username, password='1234')
        response = self.client.post('/products/add_to_card/', data={'product': product.pk, 'quantity': 1, })
        after_count = OrderItem.objects.count()
        assert response.status_code == 302
        assert after_count - 1 == start_count
