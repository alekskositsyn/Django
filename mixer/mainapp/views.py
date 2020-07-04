import random

from django.shortcuts import render, get_object_or_404
from mainapp.models import ProductCategory, Product


def get_hot_product():
    hot_product_pk = random.choice(Product.objects.values_list('pk', flat=True))
    hot_product = Product.objects.get(pk=hot_product_pk)
    return hot_product


def get_basket(request):
    return request.user.is_authenticated and request.user.basket.all() or []


def get_menu():
    return ProductCategory.objects.all()


def home(request):
    context = {
        'page_title': 'главная "mixer"',
        'basket': get_basket(request),
    }
    return render(request, 'mainapp/home.html', context)


def catalog(request):
    products = Product.objects.all()

    context = {
        'page_title': 'каталог',
        'products_categories': get_menu(),
        'products': products,
        'basket': get_basket(request),
    }
    return render(request, 'mainapp/catalog.html', context)


def category_products(request, pk):
    if pk == '0':
        category = {'pk': 0, 'name': 'все'}
        products = Product.objects.all()
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        products = category.product_set.all()

    context = {
        'page_title': 'продукты по категории',
        'products_categories': get_menu(),
        'products': products,
        'category': category,
        'basket': get_basket(request),
    }
    return render(request, 'mainapp/category_products.html', context)


def contacts(request):
    context = {
        'page_title': 'контакты',
        'basket': get_basket(request),
    }
    return render(request, 'mainapp/contacts.html', context)


def product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    same_product = get_hot_product().category.product_set.exclude(pk=get_hot_product().pk)

    context = {
        'page_title': 'каталог',
        'categories': get_menu(),
        'category': product.category,
        'basket': get_basket(request),
        'product': product,
        'hot_product': get_hot_product,
        'same_product': same_product,
    }
    return render(request, 'mainapp/product.html', context)
