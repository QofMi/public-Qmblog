from django.conf import settings
from django.contrib import messages
import requests
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

USER_DEVICE = [
"Windows Phone", "Windows",
"iPhone", "iPad", "Macintosh", "Mac OS",
"Android",
"Linux",]


# Проверка капчи
def _check_recaptcha(function):
    """
    Проверка валидности reCaptcha от Google
    """
    def wrap(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.RECAPTCHA_PRIVATE_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
                messages.error(request, 'Неверная reCaptcha. Пожалуйста, попробуйте снова.')
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def _get_client_ip(request):
    """
    Получение ip адреса клиента
    """
    x_forwarded_for = request.META.get('HTTP_X_REAL_IP')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def _get_user_agent(request):
    """
    Получение user agent'a пользователя и фильтрация полученных данных
    """
    user_agent = request.META.get('HTTP_USER_AGENT')
    length = len(USER_DEVICE)
    for i in range(0, length):
        if USER_DEVICE[i] in user_agent:
            user_agent = USER_DEVICE[i]
            return user_agent


def _send_email_message(email_subgect: str, email_html_template: str, email_parameters_rendering: None, user_email: None,) -> None:
    """
    Отправляет сообщение рассылки
    """
    email_subgect = email_subgect
    html_content = render_to_string(email_html_template, email_parameters_rendering)
    text_content = strip_tags(html_content)
    email_message = EmailMultiAlternatives(
    #Объект
    email_subgect,
    # Контент
    text_content,
    # От кого
    settings.EMAIL_HOST_USER,
    # Кому
    [user_email]
    )
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()
