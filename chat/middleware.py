import random
import hashlib
import time
from lazysignup.decorators import allow_lazy_user
from lazysignup.templatetags.lazysignup_tags import is_lazy_user
from lazysignup.models import LazyUser
from django.utils.decorators import method_decorator
from haikunator import Haikunator
from chat.models import Room, Message, CustomUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

class LazyUserMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_anonymous() and not is_lazy_user(request.user):
            new_lazy_user = self.get_or_create_guest_account(request.user, request)
            login(request, new_lazy_user.user, 'django.contrib.auth.backends.ModelBackend')
        response = self.get_response(request)
        return response

    def get_or_create_guest_account(self, user, request):
        custom_user, username = LazyUser.objects.create_lazy_user()
        haikunator = Haikunator()
        usernames = [user.username for user in CustomUser.objects.all()]
        guest_name = haikunator.haikunate(token_length=0)
        while guest_name in usernames:
            guest_name = haikunator.haikunate(token_length=0)
        custom_user.nickname = guest_name
        custom_user.save()
        new_lazy_user = LazyUser.objects.get(user__username=username)
        return new_lazy_user
