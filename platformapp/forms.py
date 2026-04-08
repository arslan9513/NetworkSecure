from django import forms
from django.contrib.auth.models import User
from .models import TrafficLog


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class TrafficUploadForm(forms.Form):
    file = forms.FileField(label='Log faýly (CSV)')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff', 'is_active']
