from django.urls import path

import ordersapp.views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderList.as_view(), name='index'),
    path('order/create/', ordersapp.OrderCreate.as_view(), name='order_create'),
    path('order/read/<int:pk>/', ordersapp.OrderRead.as_view(), name='order_read'),
    path('order/update/<int:pk>/', ordersapp.OrderUpdate.as_view(), name='order_update'),
    path('order/delete/<int:pk>/', ordersapp.OrderDelete.as_view(), name='order_delete'),
    path('order/order_forming_complete/<int:pk>/', ordersapp.order_forming_complete, name='order_forming_complete'),
]
