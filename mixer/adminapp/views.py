from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect, request
from django.shortcuts import render, get_object_or_404

from authapp.models import ShopUser
from django.urls import reverse

from adminapp.forms import AdminShopUserCreatForm

from adminapp.forms import AdminShopUserUpdateForm


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

    context = {'title': 'пользователи/создание',
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



