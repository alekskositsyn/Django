from django.urls import path

import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.UsersListView.as_view(), name='users'),
    path('user/create/', adminapp.UserCreateView.as_view(), name='user_create'),
    path('user/update/<int:pk>/', adminapp.UserUpdateView.as_view(), name='user_update'),
    path('user/delete/<int:pk>/', adminapp.UserDeleteView.as_view(), name='user_delete'),
    path('user/restore/<int:pk>/', adminapp.UserRestoreView.as_view(), name='user_restore'),

    path('categories/', adminapp.CategoriesListView.as_view(), name='categories'),
    path('categories/create/', adminapp.ProductCategoryCreateView.as_view(), name='category_create'),
    path('categories/update/<int:pk>/', adminapp.ProductCategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', adminapp.ProductCategoryDeleteVeiw.as_view(), name='category_delete'),
    path('categories/restore/<int:pk>/', adminapp.ProductCategoryRestore.as_view(), name='categories_restore'),

    path('category/<int:pk>/product/create/', adminapp.ProductCreateView.as_view(), name='product_create'),

    path('category/<int:pk>/products/', adminapp.CategoryProductsListView.as_view(), name='category_products'),

    path('products/<int:product_pk>/', adminapp.ProductDetail.as_view(), name='item_products'),
    path('products/update/<int:pk>/', adminapp.ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', adminapp.ProductDelete.as_view(), name='product_delete'),
    path('products/restore/<int:pk>/', adminapp.ProductRestore.as_view(), name='products_restore'),
]
