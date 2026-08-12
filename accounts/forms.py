from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(max_length=30, required=False, label="Ім'я")
    last_name = forms.CharField(max_length=30, required=False, label="Прізвище")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(max_length=30, required=False, label="Ім'я")
    last_name = forms.CharField(max_length=30, required=False, label="Прізвище")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')