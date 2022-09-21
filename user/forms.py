from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Users


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ['name', 'username', 'email', 'password1', 'password2']


class UserEditForm(ModelForm):
    class Meta:
        model = Users
        fields = ['photo', 'name', 'username', 'bio']


class UserSecurityForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ['email', 'password1', 'password2']
