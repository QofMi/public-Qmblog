from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.urls import reverse
from .models import Post
from .utils import *
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator


# Create your views here.

# Список постов
def posts_list(request):
    posts = Post.objects.all()

    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()
    if page.has_previous():
        previous_url = '?page={}'.format(page.previous_page_number())
    else:
        previous_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
    'page': page,
    'is_paginated': is_paginated,
    'next_url': next_url,
    'previous_url': previous_url
    }

    return render(request, 'blog/index.html', context=context)

# О Нас
def about(request):
    return render(request, 'blog/about.html')

# Создание постов
class post_create(LoginRequiredMixin, PermissionRequiredMixin, ObjectCreateMixin, View):
    form_model = PostForm
    template = 'blog/post_create_form.html'
    # raise_exception = True
    permission_required = 'blog.add_post'

# Редактирование постов
class post_update(LoginRequiredMixin, PermissionRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    form_model = PostForm
    template = 'blog/post_update_form.html'
    # raise_exception = True
    permission_required = 'blog.change_post'

# Удаление постов
class post_delete(LoginRequiredMixin, PermissionRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post_update_form.html'
    redirect_url = 'posts_list_url'
    # raise_exception = True
    permission_required = 'blog.delete_post'

# Просмотр поста
class post_detail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'

# 404
def view_404(request, exception):
    return render(request, 'errs/404.html')

# 403
def view_403(request, exception):
    return render(request, 'errs/403.html')
