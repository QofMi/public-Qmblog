from django.shortcuts import render, redirect, reverse
from .forms import *
from .services import *
from django.views.generic import View
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# Авторизация
from django.contrib.auth import authenticate, login, logout

# Профиль
from blog.models import Post

# Смена пароля
from django.contrib.auth.forms import PasswordChangeForm


class SignIn(LoginUserMixin, View):
    """
    Авторизация
    """
    form_model = LoginUserForm
    template = 'accounts/sign_in.html'
    redirect_url = 'home_url'
    redirect_url_is_authenticated = 'user_profile_url'


class SignUp(CreateUserMixin, View):
    """
    Регистрация
    """
    form_model = CreateUserForm
    template = 'accounts/sign_up.html'
    redirect_url = 'sign_in_url'
    redirect_url_is_authenticated = 'user_profile_url'


class UsernameValidationView(ValidationMixin, View):
    pass 


def privacy_policy(request):
    """
    Политика конфиденциальности
    """
    return render(request, 'accounts/policy.html')


def logout_user(request):
    """
    Выход из системы
    """
    logout(request)
    return redirect(reverse('home_url'))


class ActivateUserAccounts(ActivateUser, View):
    """
    Активация
    """
    template = 'accounts/activate_fail.html'
    redirect_url = 'sign_in_url'


class UserProfile(LoginRequiredMixin, UserProfileMixin, View):
    """
    Профиль пользователя
    """
    model = Post
    template = 'accounts/user_profile.html'


class UserProfileUpdate(LoginRequiredMixin, UserProfileUpdateMixin, View):
    """
    Редактирование профиля
    """
    template = 'accounts/user_profile_edit.html'
    form_model = UserProfileUpdateForm
    redirect_url = 'user_profile_url'


class ChangeUserPassword(LoginRequiredMixin, ChangeUserPasswordMixin, View):
    """
    Смена пароля пользователя
    """
    template = 'accounts/user_change_password.html'
    redirect_url = 'user_profile_url'
    form_model = PasswordChangeForm
