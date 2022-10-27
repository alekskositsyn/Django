from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models import Q
from adminapp.views import db_profile_by_type
from mainapp.models import Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        test_products = Product.objects.filter(
            Q(category__name='Красители пищевые') &
            Q(price__lte='30')
        )

        db_profile_by_type(test_products, '', connection.queries)
