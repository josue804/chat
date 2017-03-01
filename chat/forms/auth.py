from django import forms
from chat.models import CustomUser
from django.core.exceptions import ValidationError

class ChatRoomForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control chatbox-form--input',
                'rows': 1,
                'cols': 40,
            }
        )
    )

class CustomUserCreateForm(forms.ModelForm):
    password_confirmation = forms.CharField(max_length=72, required=True, widget=forms.widgets.TextInput(attrs={'type': 'password'}))
    preserve_lazy_data = forms.BooleanField(label="Save all my previous messages to my new account", initial=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'username', 'password', 'password_confirmation',
            'about', 'avatar', 'preserve_lazy_data',)
        widgets = {
            'password': forms.widgets.TextInput(attrs={'type': 'password'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(CustomUser.objects.filter(username=username)) > 0:
            raise ValidationError('This username is taken')
        return self.cleaned_data['username']

    def clean(self):
        data = self.cleaned_data
        password, password_confirmation = data['password'], data['password_confirmation']
        if password == password_confirmation:
            return data
        else:
            self.add_error('password', 'Passwords do not match')
            self.add_error('password_confirmation', 'Passwords do not match')
