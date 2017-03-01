from chat.forms import CustomUserCreateForm
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

class CreateAccountView(FormView):
    template_name = "core/create-account.html"
    form_class = CustomUserCreateForm
