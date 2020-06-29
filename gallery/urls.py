from django.urls import path
from .views import *

urlpatterns = [
    path('', GalleryList.as_view(), name='home_url'),

]
