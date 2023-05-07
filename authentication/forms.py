from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Пароль", widget=forms.TextInput(attrs={'class': 'form-control',
                                                                             'type': 'password'}))

    class Meta:
        model = User
        fields = ('username', 'password')


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-control w-100'}))
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={'class': 'form-control w-100'}))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={'class': 'form-control w-100'}))
    password1 = forms.CharField(label="Пароль", widget=forms.TextInput(attrs={'class': 'form-control w-100',
                                                                              'type': 'password'}))
    password2 = forms.CharField(label="Повторите пароль", widget=forms.TextInput(attrs={'class': 'form-control w-100',
                                                                                        'type': 'password'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')