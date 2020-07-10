from django.urls import path

import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.UsersListView.as_view(), name='users'),
    path('user/create/', adminapp.UserCreateView.as_view(), name='user_create'),
    path('user/update/<int:pk>/', adminapp.UserUpdateView.as_view(), name='user_update'),
    path('user/delete/<int:pk>/', adminapp.UserDeleteView.as_view(), name='user_delete'),
    path('user/restore/<int:pk>/', adminapp.user_restore, name='user_restore'),

    path('categories/', adminapp.CategoriesListView.as_view(), name='categories'),
    path('categories/create/', adminapp.ProductCategoryCreateView.as_view(), name='category_create'),
    path('categories/update/<int:pk>/', adminapp.ProductCategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', adminapp.ProductCategoryDelete.as_view(), name='category_delete'),

    path('category/<int:category_pk>/product/create/', adminapp.product_create, name='product_create'),
    path('category/<int:pk>/products/', adminapp.category_products, name='category_products'),
    path('products/<int:pk>/', adminapp.ProductDetail.as_view(), name='item_products'),
    path('products/update/<int:pk>/', adminapp.product_update, name='product_update'),
    path('products/delete/<int:pk>/', adminapp.product_delete, name='product_delete'),
]
