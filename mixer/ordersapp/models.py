from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from authapp.models import ShopUser
from mainapp.models import Product


# class OrderItemQuerySet(models.QuerySet):
#     def delete(self, *args, **kwargs):
#         for object in self:
#             object.product.quantity += object.quantity
#             object.product.save()
#         return super().delete()


class Order(models.Model):
    FORMING = 'F'
    SENT_TO_PROCEED = 'S'
    PROCEEDED = 'P'
    PAID = 'D'
    READY = 'Y'
    CANCEL = 'C'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен'),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(verbose_name='статус',
                              max_length=1,
                              choices=ORDER_STATUS_CHOICES,
                              default=FORMING)
    is_active = models.BooleanField(verbose_name='активен', default=True, db_index=True)

    # objects = OrderItemQuerySet.as_manager()

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Текущий заказ: {self.id}'

    def get_summary(self):
        items = self.orderitems.select_related()
        return {
            'total_cost': sum(list(map(lambda x: x.quantity * x.product.price,
                                       items))),
            'total_quantity': sum(list(map(lambda x: x.quantity, items)))
        }

    def get_total_quantity(self):
        items = self.orderitems.all()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.orderitems.all()
        return len(items)

    def get_total_cost(self):
        items = self.orderitems.all()
        return sum(list(map(lambda x: x.quantity * x.product.price, items)))

    # переопределяем метод, удаляющий объект
    # def delete(self):
    #     for item in self.orderitems.select_related():
    #         item.product.quantity += item.quantity
    #         item.product.save()
    #
    #     self.is_active = False
    #     self.save()


# MANY-TO-MANY
class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name="orderitems",
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                verbose_name='продукт',
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество',
                                           default=0)

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.get(pk=pk)


@receiver(pre_save, sender=OrderItem)
def product_quantity_update_save(sender, instance, **kwargs):
    if instance.pk:
        instance.product.quantity -= instance.quantity - \
                                     sender.get_item(instance.pk).quantity
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()


@receiver(pre_delete, sender=OrderItem)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()
