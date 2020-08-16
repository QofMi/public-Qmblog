from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.urls import reverse
from .models import Post
from .services import *
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class PostsList(ObjectListMixin, View):
    """
    Список постов
    """
    model = Post
    template = 'blog/index.html'
    page_count = 12
    page_name = 'page_blog'


def about(request):
    """
    Рендер страницы "О проекте"
    """
    return render(request, 'blog/about.html', context={'page_about': True})


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, ObjectCreateMixin, View):
    """
    Создание поста
    """
    form_model = PostForm
    template = 'blog/post_create_form.html'
    permission_required = 'blog.add_post'


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, ObjectUpdateMixin, View):
    """
    Обновление поста
    """
    model = Post
    form_model = PostForm
    template = 'blog/post_update_form.html'
    permission_required = 'blog.change_post'


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, ObjectDeleteMixin, View):
    """
    Удаоение поста
    """
    model = Post
    template = 'blog/post_update_form.html'
    redirect_url = 'posts_list_url'
    permission_required = 'blog.delete_post'


class PostDetail(ObjectDetailMixin, View):
    """
    Детали поста
    """
    model = Post
    template = 'blog/post_detail.html'


def view_404(request, exception):
    """
    Рендер страницы кода ошиибки 404
    """
    return render(request, 'errs/404.html')


def view_403(request, exception):
    """
    Рендер страницы кода ошибки 403
    """
    return render(request, 'errs/403.html')
