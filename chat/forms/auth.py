from django import forms
from chat.models import CustomUser

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

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'username', 'password', 'password_confirmation',
            'about', 'avatar',)
        widgets = {
            'password': forms.widgets.TextInput(attrs={'type': 'password'}),
        }

    def clean(self):
        data = self.cleaned_data
        password, password_confirmation = data['password'], data['password_confirmation']
        if password == password_confirmation:
            return data
        else:
            self.add_error('password', 'Passwords do not match')
            self.add_error('password_confirmation', 'Passwords do not match')
