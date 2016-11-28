from django import forms

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
