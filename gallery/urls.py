from django.urls import path
from .views import *

urlpatterns = [
    path('', gallery_list.as_view(), name='home_url'),

]
