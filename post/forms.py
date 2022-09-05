from django.forms import ModelForm
from post.models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('book', 'name', 'body')
