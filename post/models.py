from django.db import models

# Create your models here.
from user.models import Users


class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(to='user.Author', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    owner = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, related_name="post_owner")
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, related_name="post_book")
    name = models.CharField(max_length=200)
    body = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    likes = models.ManyToManyField(Users, related_name="post_likes")
    is_approved = models.BooleanField(default=0)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]

    def num_likes(self):
        return self.likes.count()


class Comment(models.Model):
    owner = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    body = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]

