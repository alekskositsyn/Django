from django.db import models
from django.utils.functional import cached_property
from authapp.models import ShopUser
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('количество', default=0)
    add_datetime = models.DateTimeField('время', auto_now_add=True)

    @cached_property
    def get_item_cached(self):
        return self.user.basket.select_related().all()

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        return sum(map(lambda x: x.quantity, self.get_item_cached))

    @property
    def total_cost(self):
        return sum(map(lambda x: x.product_cost, self.get_item_cached))

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)

    def delete(self, using=None, keep_parents=False):
        self.product.quantity += self.quantity
        self.product.save()
        return super().delete(using=None, keep_parents=False)
