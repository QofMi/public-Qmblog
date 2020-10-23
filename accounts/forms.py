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
            'username': forms.TextInput(attrs={'placeholder': 'Имя пользователя', 'class': 'signin__input', 'id': 'signup_username', 'alt': 'Имя пользователя', 'required': ''}),

            'email': forms.TextInput(attrs={'placeholder': 'Адрес эл. почты', 'class': 'signin__input', 'alt': 'Адрес эл. почты', 'required': ''}),

            'first_name': forms.TextInput(attrs={'placeholder': 'Имя', 'class': 'signin__input', 'alt': 'Имя', 'required': ''}),

            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия', 'class': 'signin__input', 'alt': 'Фамилия', 'required': ''}),

        }
