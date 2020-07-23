from django.urls import path

import ordersapp.views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.index, name='index'),
    # path('add/product/<int:pk>/', ordersapp.add_product, name='add_product'),
    # path('delete/product/<int:pk>/', ordersapp.delete_product, name='delete_product'),
    # path('change/<int:pk>/quantity/<int:quantity>/', ordersapp.change),
]
