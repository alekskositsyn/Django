def products_categories(request):
    products_categories = request.ProductCategory.objects.filter(is_active=True)

    return {
        'products_categories': products_categories,
    }
