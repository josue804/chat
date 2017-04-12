from django.contrib.auth import authenticate, login
from chat.forms import CustomUserCreateForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from chat.models import GuestUser, Message, CustomUser
from lazysignup.utils import is_lazy_user
from lazysignup.models import LazyUser

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
        initial['username'] = self.request.user.get_username()
        return initial

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            user.nickname = self.request.user.nickname
            user.set_password(form.cleaned_data['password'])
            user.save()
            for message in Message.objects.filter(user=self.request.user):
                message.user = user
                message.handle = user.username
                message.save()
            LazyUser.objects.get(user=self.request.user).delete()
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('chat:chat-dashboard')

class AccountDetailView(TemplateView):
    template_name = "account/account-detail.html"

    def get_context_data(self, *args, **kwargs):
        kwargs = super(AccountDetailView, self).get_context_data(*args, **kwargs)
        kwargs['profile'] = CustomUser.objects.get(pk=kwargs['pk'])
        return kwargs
