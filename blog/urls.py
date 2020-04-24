from django.urls import path
from .views import *




urlpatterns = [
    path('', posts_list, name='posts_list_url'),
    path('create/', post_create.as_view(), name='posts_create_url'),
    path('<str:slug>/', post_detail.as_view(), name='post_detail_url'),
    path('<str:slug>/update/', post_update.as_view(), name='post_update_url'),
    path('<str:slug>/delete/', post_delete.as_view(), name='post_delete_url'),
    path('about', about, name='about_url'),
#    path('tags/', tags_list, name='tags_list_url'),
#    path('tag/<str:slug>', tag_detail.as_view(), name='tag_detail_url')

]
