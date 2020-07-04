from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import ShopUserLoginForm

from authapp.forms import ShopUserRegisterForm

from authapp.forms import ShopUserUpdateForm


def login(request):
    # next = request.GET['next'] if 'next' in request.GET.keys() else ''
    next = request.GET.get('next', '')
    if request.method == 'POST':
        form = ShopUserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                if 'next' in request.POST.keys():
                    return HttpResponseRedirect(request.POST['next'])
                else:
                    return HttpResponseRedirect(reverse('main:home'))
    else:
        form = ShopUserLoginForm()
    # form = ShopUserLoginForm()
    context = {
        'title': 'вход в ситему',
        'form': form,
        'next': next,
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:home'))


def register(request):
    if request.method == 'POST':
        form = ShopUserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('main:home'))
    else:
        form = ShopUserRegisterForm()
    context = {
        'title': 'Проверьте правильность заполнения данных',
        'form': form,
    }
    return render(request, 'authapp/register.html', context)


def update(request):
    if request.method == 'POST':
        form = ShopUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:update'))
    else:
        form = ShopUserUpdateForm(instance=request.user)
    context = {
        'title': 'Проверьте правильность заполнения данных',
        'form': form,
    }
    return render(request, 'authapp/update.html', context)
