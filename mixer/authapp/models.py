from django.db import models

from django.contrib.auth.models import AbstractUser


class ShopUser(AbstractUser):
    age = models.PositiveIntegerField(verbose_name='возраст', null=True)
    avatar = models.ImageField(upload_to='users_avatar', blank=True)
