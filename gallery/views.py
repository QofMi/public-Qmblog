from .models import Gallery
from django.views.generic import View
from blog.utils import ObjectListMixin

# Create your views here.

class gallery_list(ObjectListMixin, View):
    model = Gallery
    template = 'home.html'
    page_count = 27
