from django.contrib.auth.decorators import user_passes_test
from django.db import connection
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import AdminProductCategoryUpdateForm
from adminapp.forms import AdminProductUpdateForm
from adminapp.forms import AdminShopUserCreatForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


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

    def get_queryset(self):
        qs = super().get_queryset()
        users_sort = qs.order_by('-is_superuser',
                                 '-is_staff',
                                 '-is_active',
                                 '-first_name',
                                 )
        return users_sort


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


class UserRestoreView(SuperUserOnlyMixin, DeleteView):
    model = ShopUser
    success_url = reverse_lazy('adminapp:users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class CategoriesListView(SuperUserOnlyMixin, PageTitleMixin, ListView):
    model = ProductCategory
    page_title = 'админка/категории'


class ProductCategoryCreateView(SuperUserOnlyMixin, PageTitleMixin, CreateView):
    model = ProductCategory
    form_class = AdminProductCategoryUpdateForm
    page_title = 'категории/создание'
    success_url = reverse_lazy('adminapp:categories')


class ProductCategoryUpdateView(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = ProductCategory
    form_class = AdminProductCategoryUpdateForm
    page_title = 'категории/редактирование'
    success_url = reverse_lazy('adminapp:categories')

    """ Функция применяет скидку к цене продукта, если скидка есть"""

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))

        return super().form_valid(form)


class ProductCategoryDeleteVeiw(SuperUserOnlyMixin, DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('adminapp:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        result = super().get_success_url()
        # print(vars(self))
        # print(dir(self))
        return result


class ProductCategoryRestore(SuperUserOnlyMixin, DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('adminapp:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class CategoryProductsListView(ListView):
    def get_queryset(self):
        obj = Product.objects.filter(category__pk=self.kwargs['pk']).order_by('-is_active', 'name')
        return obj

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['category'] = ProductCategory.objects.get(pk=self.kwargs['pk'])
        context['title'] = 'категория/продукты'
        return context


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
    model = Product
    form_class = AdminProductUpdateForm
    page_title = 'продукт/создание'

    def get_success_url(self):
        return reverse('my_admin:category_products', kwargs={'pk': self.object.category.pk})


class ProductDetail(DetailView, PageTitleMixin):
    model = Product
    pk_url_kwarg = 'product_pk'
    page_title = 'продукт'


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

    def get_success_url(self):
        return reverse('my_admin:category_products', kwargs={'pk': self.object.category.pk})


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

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('my_admin:category_products', kwargs={'pk': self.object.category.pk})


class ProductRestore(SuperUserOnlyMixin, DeleteView):
    model = Product

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('my_admin:category_products', kwargs={'pk': self.object.category.pk})


def db_profile_by_type(prefix, query_type, queries):
    """отфильтровывает запросы определенного типа
    («UPDATE», «DELETE», «SELECT», «INSERT INTO») и выводит их текст в консоль"""
    update_queries = list(filter(lambda x: query_type in x['sql'], queries))
    print(f'db_profile {query_type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(post_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    """Если поле в категории is_active изменится, функция меняет в поле статус всех товаров измененной категории"""
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)
