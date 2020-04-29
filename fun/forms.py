from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)


class AuthorForm(forms.Form):
    nickname = forms.CharField(label="nickname", max_length=20)
    count_posts = forms.IntegerField(label="count_posts")
    about = forms.CharField(max_length=500, widget=forms.Textarea)


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=50, required=True, widget=forms.EmailInput(attrs={"class": "myfield"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "myfield"}), label='Имя пользователя')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "myfield"}), label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "myfield"}), label='Повторите пароль')

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')


class PostForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(max_length=20000, widget=forms.Textarea)
    theme = forms.CharField(max_length=300)
    tags = forms.CharField(max_length=300)
