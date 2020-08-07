from django.urls import path, re_path
from django.views.decorators.cache import cache_page
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.home, name='home'),
    path('catalog/', mainapp.catalog, name='catalog'),
    re_path(r'^category/(?P<pk>\d+)/products/$', mainapp.category_products, name='category_products'),
    re_path(r'^category/(?P<pk>\d+)/products/ajax/$',
            cache_page(3600, key_prefix='mixer')(mainapp.category_products_ajax)),
    re_path(r'^category/(?P<pk>\d+)/products/(?P<page>\d+)/$',
            mainapp.category_products, name='category_products'),
    re_path(r'^category/(?P<pk>\d+)/products/(?P<page>\d+)/ajax/$',
            cache_page(3600, key_prefix='mixer')(mainapp.category_products_ajax)),
    path('contacts/', mainapp.contacts, name='contacts'),
    re_path(r'^product/(?P<pk>\d+)/$', mainapp.product, name='product'),
    re_path(r'^product/detail/(?P<pk>\d+)/async/$', mainapp.product_detail_async),
]
