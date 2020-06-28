from django.shortcuts import render, get_object_or_404
from mainapp.models import ProductCategory, Product


def home(request):
    context = {
        'page_title': 'главная "mixer"',
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


def category_products(request, pk):
    categories = ProductCategory.objects.all()
    if pk == '0':
        category = {'pk': 0, 'name': 'все'}
        products = Product.objects.all()
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        products = category.product_set.all()

    context = {
        'page_title': 'продукты по категории',
        'products_categories': categories,
        'products': products,
        'category': category,
    }
    return render(request, 'mainapp/category_products.html', context)


def contacts(request):
    context = {
        'page_title': 'контакты'
    }
    return render(request, 'mainapp/contacts.html', context)


def product(request):
    first_product = Product.objects.all()[0]
    context = {
        'page_title': 'продукт',
        'first_product': first_product,
    }
    return render(request, 'mainapp/product.html', context)
