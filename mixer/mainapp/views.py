from django.shortcuts import render
from mainapp.models import ProductCategory, Product

def home(request):
    context = {
        'page_title': 'главная "mixer"'
    }
    return render(request, 'mainapp/home.html', context)


def catalog(request):
    categories = ProductCategory.objects.all()
    products = Product.objects.all()

    context = {
        'page_title': 'каталог',
        'products_categories': categories,
        'products': products,
    }
    return render(request, 'mainapp/catalog.html', context)


def contacts(request):
    context = {
        'page_title': 'контакты'
    }
    return render(request, 'mainapp/contacts.html', context)


def product(request):
    context = {
        'page_title': 'продукт'
    }
    return render(request, 'mainapp/product.html', context)
