from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import *
from gallery.models import *
from django.core.exceptions import PermissionDenied
from .images import compress
from django.core.paginator import Paginator
# Create ur utils here.

class ObjectListMixin:
    model = None
    template = None
    page_count = None
    page_name = None

    def get(self, request):
        object = self.model.objects.all()

        paginator = Paginator(object, self.page_count)
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
        'previous_url': previous_url,
        self.page_name: True
        }

        return render(request, self.template, context=context)

class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, slug):
        object = get_object_or_404(self.model, slug__iexact=slug)
        return render(request, self.template, context={
        self.model.__name__.lower(): object,
        'admin_object': object,
        'detail': True
        })

class ObjectCreateMixin:
    form_model = None
    template = None

    def get(self, request):
        form = self.form_model()
        return render(request, self.template, context={'form': form})

    def post(self, request):
        form = self.form_model(request.POST, request.FILES)
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.user = request.user
            if new_object.img:
                new_object.img = compress(new_object.img)
            new_object.save()
            return redirect(new_object)
        return render(request, self.template, context={'form': form})

class ObjectUpdateMixin:
    model = None
    template = None
    form_model = None

    def get(self, request, slug):
        object = self.model.objects.get(slug__iexact=slug)
        form = self.form_model(instance=object)
        if request.user.groups.filter(name="Модераторы").exists():
            if object.user != self.request.user:
                raise PermissionDenied
            return render(request, self.template, context={'form': form, self.model.__name__.lower(): object})
        if request.user.groups.filter(name="Администраторы").exists() or request.user.is_superuser:
            return render(request, self.template, context={'form': form, self.model.__name__.lower(): object})

    def post(self, request, slug):
        object = self.model.objects.get(slug__iexact=slug)
        form = self.form_model(request.POST, request.FILES, instance=object)

        if form.is_valid():
            new_object = form.save(commit=False)
            try:
                objects = Post.objects.get(slug__iexact=slug)
                if new_object.img != objects.img:
                    objects.img.delete()
                    new_object.img = compress(new_object.img)
            except:
                pass
            new_object.save()
            return redirect(new_object)
        return render(request, self.template, context={'form': form, self.model.__name__.lower(): object})

class ObjectDeleteMixin:
    model = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        object = self.model.objects.get(slug__iexact=slug)
        if request.user.groups.filter(name="Модераторы").exists():
            if object.user != self.request.user:
                raise PermissionDenied
            return render(request, self.template, context={self.model.__name__.lower(): object})
        if request.user.groups.filter(name="Администраторы").exists() or request.user.is_superuser:
            return render(request, self.template, context={self.model.__name__.lower(): object})


    def post(self, request, slug):
        object = self.model.objects.get(slug__iexact=slug)
        object.delete()
        return redirect(reverse(self.redirect_url))
