from django.test import TestCase

from mainapp.models import Product, ProductCategory


class ProductsTestCase(TestCase):
    def setUp(self):
        category = ProductCategory.objects.create(name="Красители пищевые")
        self.product_1 = Product.objects.create(
            name="Черный краситель",
            category=category,
            price=19.5,
            quantity=150
        )
        self.product_2 = Product.objects.create(
            name="Синий краситель",
            category=category,
            price=29.1,
            quantity=125,
            is_active=False
        )
        self.product_3 = Product.objects.create(
            name="Розовый краситель",
            category=category,
            price=98.1,
            quantity=115
        )

    def test_product_get(self):
        product_1 = Product.objects.get(name="Черный краситель")
        product_2 = Product.objects.get(name="Синий краситель")
        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)

    def test_product_print(self):
        product_1 = Product.objects.get(name="Черный краситель")
        product_2 = Product.objects.get(name="Синий краситель")
        self.assertEqual(str(product_1), 'Черный краситель (Красители пищевые)')
        self.assertEqual(str(product_2), 'Синий краситель (Красители пищевые)')

    def test_product_get_items(self):
        product_1 = Product.objects.get(name="Черный краситель")
        product_3 = Product.objects.get(name="Розовый краситель")
        products = Product.get_active_items()

        self.assertEqual(list(products), [product_1, product_3])
