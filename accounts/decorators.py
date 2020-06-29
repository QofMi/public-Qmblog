from django.conf import settings
from django.contrib import messages
import requests


# Проверка капчи
def check_recaptcha(function):
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


def get_client_ip(request):
    """
    Получение ip адреса клиента
    """
    x_forwarded_for = request.META.get('HTTP_X_REAL_IP')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    """
    Получение user agent'a пользователя и фильтрация полученных данных
    """
    user_agent = request.META.get('HTTP_USER_AGENT')
    if 'Windows NT' in user_agent:
        user_agent = 'Windows'
    elif 'Linux' and 'Android' in user_agent:
        user_agent = 'Android'
    elif 'Linux' in user_agent:
        user_agent = 'Linux'
    elif 'iPhone' in user_agent:
        user_agent = 'iPhone'
    elif 'iPad' in user_agent:
        user_agent = 'iPad'
    elif 'Macintosh' and 'Mac OS' in user_agent:
        user_agent = 'Mac'
    else:
        user_agent = 'None'
    return user_agent
