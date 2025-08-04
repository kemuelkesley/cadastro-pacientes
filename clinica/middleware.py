import time
from django.conf import settings
from django.contrib.auth import logout

# Middleware automatico para deslogar o usuario após um período de inatividade
# Este middleware verifica a atividade do usuário e desloga automaticamente se o tempo limite for atingido
class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_time = int(time.time())
            last_activity = request.session.get('last_activity', current_time)
            if current_time - last_activity > settings.SESSION_COOKIE_AGE:
                logout(request)
            else:
                request.session['last_activity'] = current_time
        return self.get_response(request)
