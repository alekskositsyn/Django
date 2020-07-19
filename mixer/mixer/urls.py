from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('', include('mainapp.urls', namespace='main')),
    path('auth/', include('authapp.urls', namespace='auth')),
    # re_path(r'^auth/verify/google/oauth2/', include("social_django.urls", namespace="social")),
    path('auth/register/', include('social_django.urls', namespace='social')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('my/admin/', include('adminapp.urls', namespace='my_admin')),

    path('admin/', admin.site.urls, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
