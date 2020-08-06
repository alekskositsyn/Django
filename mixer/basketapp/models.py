from django.db import models
from django.utils.functional import cached_property

from authapp.models import ShopUser

from mainapp.models import Product


# class BasketQuerySet(models.QuerySet):  # own model manager
#     def delete(self):
#         for object in self:
#             # object.product.quantity += object.quantity
#             # object.product.save()
#             object.delete()
#         return super().delete()


class Basket(models.Model):
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('количество', default=0)
    add_datetime = models.DateTimeField('время', auto_now_add=True)

    # objects = BasketQuerySet.as_manager()
    @cached_property
    def get_item_cached(self):
        return self.user.basket.select_related().all()

    @property
    def product_cost(self):
        "return cost of all products this type"
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        # return sum(self.user.basket.values_list('quantity', flat=True))
        # "return total quantity for user"
        # _items = Basket.objects.filter(user=self.user)
        return sum(map(lambda x: x.quantity, self.get_item_cached))
        # return _totalquantity

    @property
    def total_cost(self):
        "return total cost for user"
        # _items = Basket.objects.filter(user=self.user)
        # _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        return sum(map(lambda x: x.product_cost, self.get_item_cached))

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)

    def delete(self, using=None, keep_parents=False):
        self.product.quantity += self.quantity
        self.product.save()
        return super().delete(using=None, keep_parents=False)

    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         self.product.quantity -= self.quantity - \
    #                                  self.__class__.get_item(self.pk).quantity
    #     else:
    #         self.product.quantity -= self.quantity
    #     self.product.save()
    #     super(self.__class__, self).save(*args, **kwargs)
