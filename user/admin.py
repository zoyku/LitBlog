from django.contrib import admin
from .models import Users, Book, Author

# Register your models here.

admin.site.register(Users)
admin.site.register(Book)
admin.site.register(Author)
