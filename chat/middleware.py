from lazysignup.decorators import allow_lazy_user
from lazysignup.templatetags.lazysignup_tags import is_lazy_user
from django.utils.decorators import method_decorator
from haikunator import Haikunator
from chat.models import Room, Message, GuestUser

class LazyUserMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if is_lazy_user(request.user):
            lazy_user = self.get_or_create_guest_account(request.user, request)
        request.lazy_username = lazy_user.username
        request.lazy_token = lazy_user.temp_token
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1]
        else:
            ip = request.META.get('REMOTE_ADDR')
        request.session['client_ip'] = ip
        return ip

    def get_or_create_guest_account(self, user, request):
        client_ip = self.get_client_ip(request)
        try:
            guest_user = GuestUser.objects.get(ip_address=client_ip)
            return guest_user
        except:
            haikunator = Haikunator()
            guest_name = haikunator.haikunate(token_length=0)
            guest_user = GuestUser.objects.create(username=guest_name, temp_token=user.username, ip_address=client_ip)
            return guest_user
