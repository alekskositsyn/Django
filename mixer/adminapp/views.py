from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect, request
from django.shortcuts import render, get_object_or_404

from authapp.models import ShopUser
from django.urls import reverse, reverse_lazy
from adminapp.forms import AdminProductUpdateForm
from adminapp.forms import AdminProductCategoryUpdateForm
from adminapp.forms import AdminShopUserCreatForm
from adminapp.forms import AdminShopUserUpdateForm
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from mainapp.models import ProductCategory, Product


# @user_passes_test(lambda x: x.is_superuser)
# def index(request):
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#     context = {
#         'title': 'админка/пользователи',
#         'object_list': users_list,
#     }
#     return render(request, 'adminapp/shopuser_list.html', context)


class SuperUserOnlyMixin:
    @method_decorator(user_passes_test(lambda x: x.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PageTitleMixin:
    page_title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.page_title
        return context


class UsersListView(SuperUserOnlyMixin, PageTitleMixin, ListView):
    model = ShopUser
    page_title = 'админка/пользователи'
    # template_name = 'adminapp/shopuser_list.html'

    # @method_decorator(user_passes_test(lambda u: u.is_superuser))
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)


# def user_create(request):
#     if request.method == 'POST':
#         user_form = AdminShopUserCreatForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('adminapp:users'))
#     else:
#         user_form = AdminShopUserCreatForm()
#
#     context = {
#         'title': 'пользователи/создание',
#         'form': user_form,
#     }
#
#     return render(request, 'adminapp/templates/authapp/shopuser_form.html', context)


class UserCreateView(SuperUserOnlyMixin, PageTitleMixin, CreateView):
    model = ShopUser
    form_class = AdminShopUserCreatForm
    page_title = 'пользователь/создание'
    success_url = reverse_lazy('adminapp:users')


class UserUpdateView(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = ShopUser
    form_class = AdminShopUserCreatForm
    page_title = 'пользователь/редактирование'
    success_url = reverse_lazy('adminapp:users')


class UserDeleteView(SuperUserOnlyMixin, DeleteView):
    model = ShopUser
    success_url = reverse_lazy('adminapp:users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# @user_passes_test(lambda x: x.is_superuser)
# def user_update(request, pk):
#     user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         user_form = AdminShopUserUpdateForm(request.POST, request.FILES, instance=user)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('my_admin:index'))
#     else:
#         user_form = AdminShopUserUpdateForm(instance=user)
#
#     context = {
#         'title': 'пользователи/редактирование',
#         'form': user_form
#     }
#
#     return render(request, 'adminapp/templates/authapp/shopuser_form.html', context)


# @user_passes_test(lambda x: x.is_superuser)
# def user_delete(request, pk):
#     user = get_object_or_404(ShopUser, pk=pk)
#     # user.delete()  # not good
#
#     if request.method == 'POST':
#         user.is_active = False
#         user.save()
#         return HttpResponseRedirect(reverse('my_admin:index'))
#
#     context = {
#         'title': 'пользователи/удаление',
#         'user_to_delete': user,
#     }
#     return render(request, 'adminapp/shopuser_confirm_delete.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_restore(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('adminapp:users'))

    context = {
        'title': 'пользователи/восстановление',
        'user_to_restore': user,
    }
    return render(request, 'adminapp/user_restore.html', context)


# @user_passes_test(lambda x: x.is_superuser)
# def categories(request):
#     categories_list = ProductCategory.objects.all()
#
#     content = {
#         'title': 'админка/категории',
#         'categories': categories_list,
#     }
#
#     return render(request, 'adminapp/templates/mainapp/productcategory_list.html', content)


class CategoriesListView(SuperUserOnlyMixin, PageTitleMixin, ListView):
    model = ProductCategory
    page_title = 'админка/категории'


# def category_create(request):
#     if request.method == 'POST':
#         category_form = ProductCategoryUpdateForm(request.POST, request.FILES)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('my_admin:categories'))
#     else:
#         category_form = ProductCategoryUpdateForm()
#
#     context = {
#         'title': 'категории/создание',
#         'form': category_form
#     }
#
#     return render(request, 'adminapp/productcategory_form.html', context)


class ProductCategoryCreateView(SuperUserOnlyMixin, PageTitleMixin, CreateView):
    model = ProductCategory
    form_class = AdminProductCategoryUpdateForm
    page_title = 'категории/создание'
    # template_name = 'adminapp/productcategory_form.html'
    success_url = reverse_lazy('adminapp:categories')
    # fields = '__all__'


class ProductCategoryUpdateView(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = ProductCategory
    form_class = AdminProductCategoryUpdateForm
    page_title = 'категории/редактирование'
    # fields = '__all__'
    # template_name = 'adminapp/templates/mainapp/productcategory_form.html'
    success_url = reverse_lazy('adminapp:categories')


# @user_passes_test(lambda x: x.is_superuser)
# def category_update(request, pk):
#     category = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         category_form = ProductCategoryUpdateForm(request.POST, request.FILES, instance=category)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('my_admin:categories'))
#     else:
#         category_form = ProductCategoryUpdateForm(instance=category)
#
#     context = {
#         'title': 'категории/редактирование',
#         'form': category_form
#     }
#
#     return render(request, 'adminapp/productcategory_form.html', context)


# @user_passes_test(lambda x: x.is_superuser)
# def category_delete(request, pk):
#     category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         category.is_active = False
#         category.save()
#         return HttpResponseRedirect(reverse('my_admin:categories'))
#
#     context = {
#         'title': 'категории/удаление',
#         'category_to_delete': category,
#     }
#     return render(request, 'adminapp/category_delete.html', context)


class ProductCategoryDelete(SuperUserOnlyMixin, DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('adminapp:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@user_passes_test(lambda x: x.is_superuser)
def categories_restore(request, pk):
    obj = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        obj.is_active = True
        obj.save()
        return HttpResponseRedirect(reverse('adminapp:categories'))

    context = {
        'title': 'категории/восстановление',
        'object': obj,
    }
    return render(request, 'adminapp/categories_restore.html', context)


@user_passes_test(lambda x: x.is_superuser)
def category_products(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    object_list = Product.objects.filter(category__pk=pk).order_by('name')

    content = {
        'title': f'продукты категории {category.name}',
        'category': category,
        'object_list': object_list,
    }

    return render(request, 'adminapp/category_products.html', content)




# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request, pk):
#     category = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         form = AdminProductUpdateForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse(
#                 'my_admin:category_products',
#                 kwargs={'pk': pk}
#             ))
#     else:
#         form = AdminProductUpdateForm(
#             initial={
#                 'category': category,
#                 # 'quantity': 10,
#                 # 'price': 157.9,
#             }
#         )
#
#     context = {
#         'title': 'продукты/создание',
#         'form': form,
#         'category': category,
#     }
#     return render(request, 'adminapp/product_form.html', context)

class ProductCreateView(SuperUserOnlyMixin, PageTitleMixin, CreateView):
    model = ProductCategory
    form_class = AdminProductUpdateForm
    page_title = 'продукт/создание'
    # template_name = 'adminapp/productcategory_form.html'
    success_url = reverse_lazy('adminapp:category_products')
    # fields = '__all__'


class ProductDetail(DetailView):
    model = Product
    # pk_url_kwarg = 'product_pk'


# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#         form = AdminProductUpdateForm(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse(
#                 'my_admin:category_products',
#                 kwargs={'pk': product.category.pk}
#             ))
#     else:
#         form = AdminProductUpdateForm(instance=product)
#
#     context = {
#         'title': 'продукты/редактирование',
#         'form': form,
#         'category': product.category,
#     }
#     return render(request, 'adminapp/templates/mainapp/product_form.html', context)


class ProductUpdateView(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = Product
    form_class = AdminProductUpdateForm
    page_title = 'продукт/редактирование'
    # fields = '__all__'
    # template_name = 'adminapp/templates/mainapp/productcategory_form.html'
    success_url = reverse_lazy('adminapp:category_products')


# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request, pk):
#     obj = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         obj.is_active = not obj.is_active
#         obj.save()
#         return HttpResponseRedirect(reverse('my_admin:category_products', kwargs={'pk': obj.category.pk}))
#
#     context = {
#         'title': 'продукты/удаление',
#         'object': obj,
#     }
#     return render(request, 'adminapp/product_confirm_delete.html', context)


class ProductDelete(SuperUserOnlyMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('adminapp:category_products')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


def products_restore(request, pk):
    obj = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        obj.is_active = True
        obj.save()
        return HttpResponseRedirect(reverse('adminapp:category_products'))

    context = {
        'title': 'категории/восстановление',
        'object': obj,
    }
    return render(request, 'adminapp/products_restore.html', context)
