from django.contrib.auth import authenticate, login
from chat.forms import CustomUserCreateForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from chat.models import GuestUser, Message, CustomUser
from lazysignup.utils import is_lazy_user

class CreateAccountView(FormView):
    template_name = "core/create-account.html"
    form_class = CustomUserCreateForm

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous() or is_lazy_user(request.user):
            return super(CreateAccountView, self).get(request, *args, **kwargs)
        else:
            return redirect('dashboard')

    def get_initial(self):
        initial = super(CreateAccountView, self).get_initial()
        initial['username'] = self.request.lazy_username
        return initial

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            if form.cleaned_data['preserve_lazy_data']:
                lazy_username = self.kwargs['slug']
                lazy_token = self.kwargs['token']
                temp_user = GuestUser.objects.get(username=lazy_username, temp_token=lazy_token)
                for message in Message.objects.filter(handle=temp_user.username):
                    message.handle = user.username
                    message.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('chat:chat-dashboard')
