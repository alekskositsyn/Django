from django.test import TestCase
from django.urls import reverse

from mainapp.models import Product, ProductCategory


class TestMainappSmoke(TestCase):
    fixtures = ['mainapp.json']

    # def setUp(self):
    #     call_command('flush', '--noinput')
    #     call_command('loaddata', 'test_db.json')
    #     self.client = Client()

    def test_mainapp_common_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # response = self.client.get('/contact/')
        response = self.client.get(reverse('main:contacts'))
        self.assertEqual(response.status_code, 200)

    def test_mainapp_catalog_urls(self):
        # response = self.client.get('/products/')
        # self.assertEqual(response.status_code, 200)

        response = self.client.get('/category/0/products/')
        self.assertEqual(response.status_code, 200)

        for category in ProductCategory.objects.all():
            response = self.client.get(f'/category/{category.pk}/products/')
            self.assertEqual(response.status_code, 200)

        for product in Product.objects.all():
            response = self.client.get(f'/product/{product.pk}/')
            self.assertEqual(response.status_code, 200)

    # def tearDown(self):
    #     call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')
