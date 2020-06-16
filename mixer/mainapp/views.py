from django.shortcuts import render


def home(request):
    return render(request, 'mainapp/home.html')


def catalog(request):
    return render(request, 'mainapp/catalog.html')


def contacts(request):
    return render(request, 'mainapp/contacts.html')


def product(request):
    return render(request, 'mainapp/product.html')
