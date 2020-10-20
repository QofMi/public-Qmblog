from django.urls import path
from .views import *


urlpatterns = [
    path('', PostsList.as_view(), name='posts_list_url'),
    path('<str:slug>/', PostDetail.as_view(), name='post_detail_url'),
    path('about', about, name='about_url'),
]
