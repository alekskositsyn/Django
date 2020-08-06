import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from mainapp.models import ProductCategory, Product
from django.core.cache import cache

from mixer.settings import LOW_CACHE


# from doc
def get_links_menu():
    if LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if LOW_CACHE:
        key = f'product_category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True,
                                              category__is_active=True
                                              ).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True,
                                      category__is_active=True
                                      ).select_related('category')


def get_product(pk):
    if LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_in_product_category(pk):
    if LOW_CACHE:
        key = f'products_in_product_category{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(
                category__pk=pk,
                is_active=True,
                category__is_active=True
            )
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(
            category__pk=pk,
            is_active=True,
            category__is_active=True
        )


# local

def get_hot_product():
    hot_product_pk = random.choice(Product.objects.values_list('pk', flat=True))
    hot_product = get_product(hot_product_pk)
    return hot_product


def home(request):
    context = {
        'page_title': 'главная "mixer"',
    }
    return render(request, 'mainapp/home.html', context)


def catalog(request):
    products = Product.objects.filter(is_active=True, category__is_active=True)

    context = {
        'page_title': 'каталог',
        'products_categories': get_links_menu(),
        'products': products,
    }
    return render(request, 'mainapp/catalog.html', context)


def category_products(request, pk, page=1):
    if pk == '0':
        category = {'pk': 0, 'name': 'все'}
        products = get_products()
    else:
        category = get_category(pk)
        products = get_products_in_product_category(pk)
    products_paginator = Paginator(products, 6)
    try:
        products = products_paginator.page(page)
    except PageNotAnInteger:
        products = products_paginator.page(1)
    except EmptyPage:
        products = products_paginator.page(products.paginator.num_pages)

    context = {
        'page_title': 'продукты по категории',
        'products_categories': get_links_menu(),
        'products': products,
        'category': category,
    }
    return render(request, 'mainapp/category_products.html', context)


def contacts(request):
    context = {
        'page_title': 'контакты',
    }
    return render(request, 'mainapp/contacts.html', context)


def product(request, pk):
    product = get_product(pk)

    same_product = get_hot_product().category.product_set.filter(
        is_active=True).select_related().exclude(pk=get_hot_product().pk)

    context = {
        'page_title': 'каталог',
        'categories': get_links_menu(),
        'category': product.category,
        'product': product,
        'hot_product': get_hot_product,
        'same_product': same_product,
    }
    return render(request, 'mainapp/product.html', context)


def product_detail_async(request, pk):
    if request.is_ajax():
        try:
            product = Product.objects.get(pk=pk)
            return JsonResponse({
                'product_price': product.price,
            })
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            })
