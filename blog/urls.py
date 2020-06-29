from django.urls import path
from .views import *


urlpatterns = [
    path('', PostsList.as_view(), name='posts_list_url'),
    path('create/', PostCreate.as_view(), name='posts_create_url'),
    path('<str:slug>/', PostDetail.as_view(), name='post_detail_url'),
    path('<str:slug>/update/', PostUpdate.as_view(), name='post_update_url'),
    path('<str:slug>/delete/', PostDelete.as_view(), name='post_delete_url'),
    path('about', about, name='about_url'),
]
