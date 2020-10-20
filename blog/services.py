from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import *
from gallery.models import *
from django.core.paginator import Paginator


class ObjectListMixin:
    """
    Отображение контента на странице с пагинацией
    """
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
    """
    Детали объекта
    """
    model = None
    template = None

    def get(self, request, slug):
        object = get_object_or_404(self.model, slug__iexact=slug)
        return render(request, self.template, context={
        self.model.__name__.lower(): object,
        'admin_object': object,
        'detail': True
        })
