from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Users, Post


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ['username', 'email', 'password1', 'password2']


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('book', 'name', 'body')
