from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.http import Http404


class SecurityAdminMiddleware(MiddlewareMixin):
    """
    Промежуточное ПО, ограничивающее доступ к административной панели.
    """
    def process_request(self, request):
        current_user = _get_current_user(request)
        if request.path.startswith(reverse('admin:index')):
            if current_user.is_authenticated:
                if not current_user.is_staff:
                    raise PermissionDenied
            else:
                raise Http404


def _get_current_user(request) -> str:
    """
    Получение текущего пользователя
    """
    request_current_user = request.user
    return request_current_user
