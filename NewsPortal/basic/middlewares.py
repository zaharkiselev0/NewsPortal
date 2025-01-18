import pytz

from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('django_timezone')  # пытаемся забрать часовой пояс из сессии
        #  если он есть в сессии, то выставляем такой часовой пояс. Если же его нет, значит он не установлен, и часовой пояс надо выставить по умолчанию (на время сервера)
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)

    def process_template_response(self, request, response):
        cur_time = timezone.localtime(timezone.now())
        theme = 'light'
        if cur_time.hour >= 19 or cur_time.hour <= 7:
            theme = 'dark'
        response.context_data['theme'] = theme
        return response
