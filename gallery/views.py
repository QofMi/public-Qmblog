from .models import Gallery
from django.views.generic import View
from blog.utils import ObjectListMixin


class GalleryList(ObjectListMixin, View):
    model = Gallery
    template = 'home.html'
    page_count = 27
    page_name = 'page_home'
