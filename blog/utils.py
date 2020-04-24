from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import *
from django.core.exceptions import PermissionDenied

# Create ur utils here.

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
            new_object = form.save()
            return redirect(new_object)
        return render(request, self.template, context={'form': form, self.model.__name__.lower(): object})

class ObjectDeleteMixin:
    model = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        object = self.model.objects.get(slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): object})

    def post(self, request, slug):
        object = self.model.objects.get(slug__iexact=slug)
        object.delete()
        return redirect(reverse(self.redirect_url))
