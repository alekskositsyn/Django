from django.urls import path, re_path

import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('add/product/<int:pk>/', basketapp.add_product, name='add_product'),
]
