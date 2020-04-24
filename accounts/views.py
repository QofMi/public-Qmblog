from django.shortcuts import render, redirect, reverse
from .forms import *
from .utils import *
from django.views.generic import View
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# Ркгистрация
from django.contrib import messages
from validate_email import validate_email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .token import generate_token
from django.core.mail import EmailMessage
from django.conf import settings

# Авторизация
from django.contrib.auth import authenticate, login, logout
# Профиль
from blog.models import Post
# Смена пароля
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.

# Авторизация
class sign_in(LoginUserMixin, View):
    form_model = LoginUserForm
    template = 'accounts/sign_in.html'
    redirect_url = 'home_url'
    redirect_url_is_authenticated = 'user_profile_url'

# Регистрация
class sign_up(CreateUserMixin, View):
    form_model = CreateUserForm
    template = 'accounts/sign_up.html'
    redirect_url = 'sign_in_url'
    redirect_url_is_authenticated = 'user_profile_url'

# Политика конфиденциальности
def Policy(request):
    return render(request, 'accounts/policy.html')

# Выход
def LogoutUser(request):
    logout(request)
    return redirect(reverse('home_url'))

# Активация
class ActivateUserAccounts(ActivateUser, View):
    template = 'accounts/activate_fail.html'
    redirect_url = 'sign_in_url'

# Профиль пользователя
class UserProfile(LoginRequiredMixin, UserProfileMixin, View):
    model = Post
    template = 'accounts/user_profile.html'


# Редактирование профиля
class UserProfileUpdate(LoginRequiredMixin, UserProfileUpdateMixin, View):
    template = 'accounts/user_profile_edit.html'
    form_model = UserProfileUpdateForm
    redirect_url = 'user_profile_url'

# Смена пароля
class ChangeUserPassword(LoginRequiredMixin, ChangeUserPasswordMixin, View):
    template = 'accounts/user_change_password.html'
    redirect_url = 'user_profile_url'
    form_model = PasswordChangeForm
