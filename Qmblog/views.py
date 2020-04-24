from django.shortcuts import render, redirect


# Create your views here.

#def redirect_blog(request):
#    return redirect('posts_list_url', permanent=True)


def home(request):
    return render(request, 'home.html')
