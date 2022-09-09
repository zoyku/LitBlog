from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Users(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    photo = models.ImageField(default="avatar.svg")
    online = models.BooleanField(default=0)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['-updated', '-date_joined']


class Book(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

