from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Users


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ['username', 'email', 'password1', 'password2']
