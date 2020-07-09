from django.urls import path, re_path

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.home, name='home'),
    path('catalog/', mainapp.catalog, name='catalog'),
    re_path(r'^category/(?P<pk>\d+)/products/$', mainapp.category_products, name='category_products'),
    re_path(r'^category/(?P<pk>\d+)/products/(?P<page>\d+)/$', mainapp.category_products, name='category_products'),
    path('contacts/', mainapp.contacts, name='contacts'),
    re_path(r'^product/(?P<pk>\d+)/$', mainapp.product, name='product'),
]
