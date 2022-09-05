from django.contrib import admin
from .models import Book, Post, Users

# Register your models here.

admin.site.register(Book)
admin.site.register(Post)
admin.site.register(Users)
