from django import forms
from .models import SocialMediaLink, Comment, CustomUser

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm




class SocialMediaLinkForm(forms.ModelForm):
    class Meta:
        model = SocialMediaLink
        fields = ['platform', 'url', 'description']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
                'username': forms.TextInput(attrs={'class': 'form-control'}),
                'email': forms.EmailInput(attrs={'class': 'form-control'}),
                'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
                'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            }

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
