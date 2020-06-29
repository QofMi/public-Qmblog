from django.urls import path
from .views import *
from .decorators import check_recaptcha

# Сброс пароля
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Логин
    path('signin/', check_recaptcha(SignIn.as_view()), name='sign_in_url'),

    # Регистрация
    path('signup/', check_recaptcha(SignUp.as_view()), name='sign_up_url'),

    # Политика конфиденцииальности
    path('policy/', policy, name='policy_url'),

    # Активация/Подтверждение почты
    path('activate/<uidb64>/<token>', ActivateUserAccounts.as_view(), name='activate'),

    # Выход
    path('logout/', logout_user, name='logout_url'),

    # Профиль пользователя
    path('user/', UserProfile.as_view(), name='user_profile_url'),

    # Редактирование пользователя
    path('user/update/', UserProfileUpdate.as_view(), name='user_profile_update_url'),

    # Смена пароля пользователя
    path('user/change-password/', ChangeUserPassword.as_view(), name='user_change_password_url'),

    # Сброс пароля
    path('reset-password/', auth_views.PasswordResetView.as_view(
    email_template_name = 'accounts/password_reset_email.html',
    template_name = 'accounts/password_reset.html'
    ), name='reset_password'),

    # Выполнена отправка сообщения/Подтверждение
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(
    template_name = 'accounts/password_reset_done.html'
    ), name='password_reset_done'),

    # Ввод нового пароля
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    template_name = 'accounts/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    # Выполнен ввод нового пароля/Подтверждение
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(
    template_name = 'accounts/password_reset_complete.html'
    ), name='password_reset_complete'),

]
