from django.shortcuts import render, redirect, reverse
from django.contrib.auth import update_session_auth_hash

# Ркгистрация
from django.contrib import messages
from validate_email import validate_email
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .token import generate_token
from django.core.mail import EmailMessage
from django.conf import settings

# Авторизация
from django.contrib.auth import authenticate, login, logout
# Create ur utils here.

# Авторизация
class LoginUserMixin:
    form_model = None
    template = None
    redirect_url = None
    redirect_url_is_authenticated = None

    def get(self, request):
        form = self.form_model()
        if not request.user.is_authenticated:
            return render(request, self.template, context={'form': form})
        else:
            return redirect(reverse(self.redirect_url_is_authenticated))

    def post(self, request):
        form = self.form_model(request.POST)
        context = {
        'form': form,
        'has_error': False
        }

        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if not user and not context['has_error']:
            messages.add_message(request, messages.ERROR, 'Неверное имя пользователя или пароль')
            context['has_error']=True

        if context['has_error']:
            return render(request, self.template, status=401, context=context)

        if self.request.recaptcha_is_valid:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect(reverse(self.redirect_url))

        return render(request, self.template, context={'form': form})

# Регистрация (создание) пользователя

class CreateUserMixin:
    form_model = None
    template = None
    redirect_url = None
    redirect_url_is_authenticated = None

    def get(self, request):
        form = self.form_model()
        if not request.user.is_authenticated:
            return render(request, self.template, context={'form': form})
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

            current_site = get_current_site(request)
            email_subgect = 'Подтвердите ваш электронный адрес'
            message = render_to_string('accounts/activate.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
            })

            email_message = EmailMessage(
            email_subgect,
            message,
            settings.EMAIL_HOST_USER,
            [email]
            )

            email_message.send()

            messages.add_message(request, messages.SUCCESS, 'Подтвердите ваш электронный адрес')
            return redirect(reverse(self.redirect_url))
        return render(request, self.template, context=context)



# Активаця пользователя
class ActivateUser:
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


# Профиль пользователя
class UserProfileMixin:
    model = None
    template = None

    def get(self, request):
        user_acc = request.user
        order_lists = self.model.objects.filter(user=user_acc).order_by('-date_pub')
        return render(request, self.template, context={'order_lists': order_lists})


# Редактирование профиля
class UserProfileUpdateMixin:
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


# Смена пароля

class ChangeUserPasswordMixin:
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
