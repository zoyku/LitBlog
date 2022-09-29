from django.db import models

# Create your models here.
from post.models import Book
from user.models import Users


class Room(models.Model):
    owner = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, related_name='room_owner')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, related_name='room_book')
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(Users, related_name='room_participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Chat(models.Model):
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='chat_room')
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]
