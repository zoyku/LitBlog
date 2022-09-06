from django.forms import ModelForm
from post.models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('book', 'name', 'body')


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
