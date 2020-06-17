from django.contrib import admin
from django.urls import path

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.home, name='home'),
    path('catalog/', mainapp.catalog, name='catalog'),
    path('contacts/', mainapp.contacts, name='contacts'),
    path('product/', mainapp.product, name='product'),
]
