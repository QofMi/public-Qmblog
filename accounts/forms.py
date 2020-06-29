from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm


class CreateUserForm(UserCreationForm, forms.Form):
    checkbox = forms.BooleanField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class UserProfileUpdateForm(UserChangeForm, forms.Form):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Имя пользователя'}),

            'email': forms.TextInput(attrs={'placeholder': 'Адрес эл. почты'}),

            'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),

            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),

        }
