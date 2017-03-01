from chat.forms import CustomUserCreateForm
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from lazysignup.decorators import allow_lazy_user
from lazysignup.templatetags.lazysignup_tags import is_lazy_user

# Create your views here.
@method_decorator(allow_lazy_user, name='dispatch')
class DashboardView(TemplateView):
    template_name = "core/dashboard.html"
