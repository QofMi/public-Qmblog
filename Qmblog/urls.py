"""Qmblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import handler404, handler403
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
import os



urlpatterns = [
#    path('', redirect_blog),
    path('', include('gallery.urls')),
    path(os.environ.get('EDITOR'), include('ckeditor_uploader.urls')),
    path(os.environ.get('ADMIN_URL'), admin.site.urls),
    path('blog/', include('blog.urls')),
    path('accounts/', include('accounts.urls'))
]

# Страницы ошибок
handler404 = 'blog.views.view_404'
handler403 = 'blog.views.view_403'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
