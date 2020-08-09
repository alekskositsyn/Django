from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserProfileUpdateForm

from authapp.forms import ShopUserRegisterForm

from authapp.forms import ShopUserUpdateForm
from authapp.models import ShopUser, ShopUserProfile


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


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:home'))


def register(request):
    if request.method == 'POST':
        form = ShopUserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            if user.send_verify_mail():
                print('сообщение подтверждения отправлено')
                return HttpResponseRedirect(reverse('auth:send_confirm'))
            else:
                print('ошибка отправки сообщения')
            # return HttpResponseRedirect(reverse('auth:login'))
            return HttpResponseRedirect(reverse('main:home'))
    else:
        form = ShopUserRegisterForm()
    context = {
        'title': 'регистрация пользователя',
        'form': form,
    }
    return render(request, 'authapp/register.html', context)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user,
                       backend='django.contrib.auth.backends.ModelBackend')
        else:
            print(f'error activation user: {user}')
        return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('main:home'))


@receiver(post_save, sender=ShopUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ShopUserProfile.objects.create(user=instance)
    else:
        instance.shopuserprofile.save()


@login_required
@transaction.atomic
def update(request):
    if request.method == 'POST':
        form = ShopUserUpdateForm(
            request.POST, request.FILES,
            instance=request.user
        )
        profile_form = ShopUserProfileUpdateForm(
            request.POST, request.FILES,
            instance=request.user.shopuserprofile
        )

        if form.is_valid() and profile_form.is_valid():
            form.save()
            # profile_form.save()
            return HttpResponseRedirect(reverse('auth:update'))
    else:
        form = ShopUserUpdateForm(instance=request.user)
        profile_form = ShopUserProfileUpdateForm(instance=request.user.shopuserprofile)
    context = {
        'title': 'Проверьте правильность заполнения данных',
        'form': form,
        'profile_form': profile_form,
    }
    return render(request, 'authapp/update.html', context)
