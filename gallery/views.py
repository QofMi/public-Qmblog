from .models import Gallery
from django.views.generic import View
from blog.services import ObjectListMixin


class GalleryList(ObjectListMixin, View):
    model = Gallery
    template = 'gallery/gallery.html'
    page_count = 27
    page_name = 'page_home'
