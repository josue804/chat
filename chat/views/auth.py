from django.contrib.auth import authenticate, login
from chat.forms import CustomUserCreateForm, CustomUserEditForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, UpdateView
from chat.models import GuestUser, Message, CustomUser
from lazysignup.utils import is_lazy_user
from lazysignup.models import LazyUser
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse
from dal import autocomplete
from chat.models import Room


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

    def get(self, request, *args, **kwargs):
        try:
            if is_lazy_user(CustomUser.objects.get(pk=kwargs['pk'])):
                return redirect(reverse('chat:chat-dashboard'))
        except:
            return redirect(reverse('chat:chat-dashboard'))
        return super(AccountDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        kwargs = super(AccountDetailView, self).get_context_data(*args, **kwargs)
        profile = CustomUser.objects.get(pk=kwargs['pk'])
        kwargs['profile'] = profile
        return kwargs

class SubscriptionsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Room.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

class AccountEditView(UpdateView):
    template_name = "account/account-edit.html"
    form_class = CustomUserEditForm
    model = CustomUser

    def get(self, request, *args, **kwargs):
        if not self.request.user.id == int(kwargs['pk']):
            return redirect(reverse('account-detail', kwargs={'pk': request.user.pk}))
        try:
            if is_lazy_user(CustomUser.objects.get(pk=kwargs['pk'])):
                return redirect(reverse('chat:chat-dashboard'))
        except:
            return redirect(reverse('chat:chat-dashboard'))
        return super(AccountEditView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            new_password = form.cleaned_data['password_reset']
            if new_password:
                user.set_password(new_password)
                user.save()
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect(reverse('account-detail', kwargs={'pk': self.request.user.pk}))
