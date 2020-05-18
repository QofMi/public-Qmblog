from django.shortcuts import render, redirect
from .models import Gallery


# Create your views here.

def home(request):
    gallery_list = Gallery.objects.all()
    return render(request, 'home.html', context={'gallery_list': gallery_list})
