from django.shortcuts import render, redirect, reverse
from django.contrib.auth import update_session_auth_hash

# Ркгистрация
from django.contrib import messages
from validate_email import validate_email
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .token import generate_token

from django.conf import settings

# Авторизация
from django.contrib.auth import authenticate, login, logout
from .utils import _get_client_ip, _get_user_agent, _send_email_message
from .models import *
from django.utils import timezone
from .secure_accounts_services import _add_ip_to_temporary_ban_ip_list, _check_status_temporary_ban_ip, _count_errors_for_temporary_ban_ip


class LoginUserMixin:
    """
    Авторизация пользователя
    """
    form_model = None
    template = None
    redirect_url = None
    redirect_url_is_authenticated = None

    def get(self, request):
        form = self.form_model()
        context = {
        'form': form,
        'public_key': settings.RECAPTCHA_PUBLIC_KEY,
        }
        if not request.user.is_authenticated:
            return render(request, self.template, context=context)
        else:
            return redirect(reverse(self.redirect_url_is_authenticated))

    def post(self, request):
        """
        Производится проверка введеных данных.
        Подсчет неудачных попытко входа и блокировка по ip адресу.
        После авторизации происходит отправка сообщения на электронную почту пользователя.
        """
        form = self.form_model(request.POST)
        context = {
        'form': form,
        'public_key': settings.RECAPTCHA_PUBLIC_KEY,
        'has_error': False
        }

        object = _add_ip_to_temporary_ban_ip_list(request)
        _check_status_temporary_ban_ip(request, object=object, template=self.template, context=context)
        if object.status is True:
            return render(request, self.template, status=401, context=context)

        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if not user and not context['has_error']:
            messages.add_message(request, messages.ERROR, 'Неверное имя пользователя или пароль')
            context['has_error']=True

        if context['has_error']:
            _count_errors_for_temporary_ban_ip(object=object)
            return render(request, self.template, status=401, context=context)

        if self.request.recaptcha_is_valid:
            if object.status == False:
                login(request, user)
                object.delete()
                _send_email_message(email_subgect='Новый вход в вашу учетную запись',
                email_html_template='accounts/hello_email.html',
                email_parameters_rendering={
                'user': user,
                'domain': get_current_site(request).domain,
                'time': timezone.now(),
                'ip_address': _get_client_ip(request),
                'user_agent': _get_user_agent(request),
                },
                user_email=user.email)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect(reverse(self.redirect_url))

        return render(request, self.template, context=context)


class CreateUserMixin:
    """
    Процесс регистрации пользователя и отправка сообщения на электронную почту для активации аккаунта
    """
    form_model = None
    template = None
    redirect_url = None
    redirect_url_is_authenticated = None

    def get(self, request):
        form = self.form_model()

        context = {
        'form': form,
        'public_key': settings.RECAPTCHA_PUBLIC_KEY,
        }

        if not request.user.is_authenticated:
            return render(request, self.template, context=context)
        else:
            return redirect(reverse(self.redirect_url_is_authenticated))

    def post(self, request):
        form = self.form_model(request.POST)

        context = {
        'form': form,
        'has_error': False
        }

        username = self.request.POST.get('username')
        email = self.request.POST.get('email')
        password1 = self.request.POST.get('password1')
        password2 = self.request.POST.get('password2')

        if len(password1)<6:
            messages.add_message(request, messages.ERROR, 'Пароль содержит менее 6 символов')
            context['has_error']=True

        if password1 != password2:
            messages.add_message(request, messages.ERROR, 'Пароли не совпадают')
            context['has_error']=True

        if not validate_email(email):
            messages.add_message(request, messages.ERROR, 'Неверный электронный адрес')
            context['has_error']=True

        try:
            if User.objects.get(email=email):
                messages.add_message(request, messages.ERROR, 'Данный электронный адрес уже существует')
                context['has_error']=True
        except Exception as identifier:
            pass

        try:
            if User.objects.get(username=username):
                messages.add_message(request, messages.ERROR, 'Данный пользователь уже существует')
                context['has_error']=True
        except Exception as identifier:
            pass

        if context['has_error']:
            return render(request, self.template, context, status=400)

        if self.request.recaptcha_is_valid:
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password1)
            user.is_active = False
            user.save()

            _send_email_message(email_subgect='Подтвердите ваш электронный адрес',
            email_html_template='accounts/activate.html',
            email_parameters_rendering={
            'user': user,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
            },
            user_email=email)

            messages.add_message(request, messages.SUCCESS, 'Подтвердите ваш электронный адрес')
            return redirect(reverse(self.redirect_url))

        return render(request, self.template, context=context)


class ActivateUser:
    """
    Проверка отправленного токена на электронную почту и активация аккаунта
    """
    template = None
    redirect_url = None

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = uid)
        except Exception as identifier:
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.INFO, 'Аккаунт создан')
            return redirect(reverse(self.redirect_url))
        return render(request, self.template, status=401)


class UserProfileMixin:
    """
    Профиль пользователя с отображением все его записей в блоге
    """
    model = None
    template = None

    def get(self, request):
        user_acc = request.user
        order_lists = self.model.objects.filter(user=user_acc).order_by('-date_pub')
        return render(request, self.template, context={'order_lists': order_lists})


class UserProfileUpdateMixin:
    """
    Обновление информации в профиле пользователя
    """
    template = None
    redirect_url = None
    form_model = None

    def get(self, request):
        form = self.form_model(instance=request.user)
        return render(request, self.template, context={'form': form})

    def post(self, request):
        form = self.form_model(request.POST, instance=request.user)

        email = self.request.POST.get('email')

        context = {
        'form': form,
        'has_error': False
        }

        if not validate_email(email):
            messages.add_message(request, messages.ERROR, 'Неверный электронный адрес')
            context['has_error']=True

        if context['has_error']:
            return render(request, self.template, context, status=400)

        if form.is_valid():
            form.save()
            return redirect(reverse(self.redirect_url))
        return render(request, self.template, context=context)


class ChangeUserPasswordMixin:
    """
    Смена пароля пользователя
    """
    template = None
    redirect_url = None
    form_model = None

    def get(self, request):
        form = self.form_model(user=request.user)
        return render(request, self.template, context={'form': form})

    def post(self, request):
        form = self.form_model(data=request.POST, user=request.user)

        context = {
        'form': form,
        'has_error': False
        }

        old_password = self.request.POST.get('old_password')
        new_password1 = self.request.POST.get('new_password1')
        new_password2 = self.request.POST.get('new_password2')

        if not request.user.check_password(old_password):
            messages.add_message(request, messages.ERROR, 'Неверный старый пароль')
            context['has_error']=True

        if new_password1 != new_password2:
            messages.add_message(request, messages.ERROR, 'Пароли не совпадают')
            context['has_error']=True

        if new_password1 == old_password:
            messages.add_message(request, messages.ERROR, 'Новый пароль не должен совпадать со старым')
            context['has_error']=True

        if context['has_error']:
            return render(request, self.template, context, status=400)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse(self.redirect_url))

        return render(request, self.template, context=context)
