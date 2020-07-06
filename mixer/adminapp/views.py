from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect, request
from django.shortcuts import render, get_object_or_404

from authapp.models import ShopUser
from django.urls import reverse

from adminapp.forms import AdminShopUserCreatForm

from adminapp.forms import AdminShopUserUpdateForm

from mainapp.models import ProductCategory

from mainapp.models import Product

from adminapp.forms import ProductCategoryUpdateForm


@user_passes_test(lambda x: x.is_superuser)
def index(request):
    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
        'title': 'админка/пользователи',
        'object_list': users_list,
    }

    return render(request, 'adminapp/index.html', context)


def user_create(request):
    if request.method == 'POST':
        user_form = AdminShopUserCreatForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('my_admin:index'))
    else:
        user_form = AdminShopUserCreatForm()

    context = {
        'title': 'пользователи/создание',
        'form': user_form,
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_update(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = AdminShopUserUpdateForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('my_admin:index'))
    else:
        user_form = AdminShopUserUpdateForm(instance=user)

    context = {
        'title': 'пользователи/редактирование',
        'form': user_form
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_delete(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)
    # user.delete()  # not good

    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('my_admin:index'))

    context = {
        'title': 'пользователи/удаление',
        'user_to_delete': user,
    }
    return render(request, 'adminapp/user_delete.html', context)


@user_passes_test(lambda x: x.is_superuser)
def categories(request):
    categories_list = ProductCategory.objects.all()

    content = {
        'title': 'админка/категории',
        'categories': categories_list,
    }

    return render(request, 'adminapp/categories.html', content)


def category_create(request):
    pass


@user_passes_test(lambda x: x.is_superuser)
def category_update(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        category_form = ProductCategoryUpdateForm(request.POST, request.FILES, instance=category)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('my_admin:categories'))
    else:
        category_form = ProductCategoryUpdateForm(instance=category)

    context = {
        'title': 'категории/редактирование',
        'form': category_form
    }

    return render(request, 'adminapp/category_update.html', context)


def category_delete(request, pk):
    pass


@user_passes_test(lambda x: x.is_superuser)
def products(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    content = {
        'title': 'админка/продукт',
        'category': category,
        'products': products_list,
    }

    return render(request, 'adminapp/products.html', content)


def product_create(request, pk):
    pass


def item_products(request, pk):
    pass


def product_update(request, pk):
    pass


def product_delete(request, pk):
    pass
