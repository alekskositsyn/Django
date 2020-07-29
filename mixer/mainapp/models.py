from django.db import models


class ProductCategory(models.Model):
    name = models.CharField('имя категории', max_length=64)
    description = models.TextField('описание категории', blank=True)  # blank=True работает на этапе валидации
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    category = models.ForeignKey(ProductCategory,
                                 on_delete=models.CASCADE,
                                 verbose_name='категория продукта')
    name = models.CharField('имя продукта', max_length=128)
    image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField(verbose_name='краткое описание продукта', max_length=64, blank=True)
    description = models.TextField(verbose_name='описание продукта', blank=True)
    price = models.DecimalField(verbose_name='цена продукта', max_digits=8, decimal_places=0, default=0)
    quantity = models.PositiveIntegerField(verbose_name='количество товара', default=0)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    @staticmethod
    def get_active_items():
        return Product.objects.filter(category__is_active=True, is_active=True)
