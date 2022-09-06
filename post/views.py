from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect

from user.models import Book
from .forms import PostForm, CommentForm
from .models import Post, Comment


class CreatePostView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        form = PostForm()
        return render(request, 'post/post_form.html', {"form": form})

    @method_decorator(login_required(login_url='login'))
    @method_decorator(csrf_protect)
    def post(self, request):
        form = PostForm(request.POST)
        book_name = request.POST.get('book')
        book, created = Book.objects.get_or_create(name=book_name)

        post = Post.objects.create(
            owner=request.user,
            book=book,
            name=request.POST.get('name'),
            body=request.POST.get('body'),
        )

        if post is not None:
            return redirect('home')

        return render(request, 'post/post_form.html', {"form": form})


class PostView(View):
    def get(self, request, p):
        post = Post.objects.get(id=p)
        comments = post.comment_set.all()
        form = CommentForm(request.POST)

        context = {'post': post, 'comments': comments, "form": form}
        return render(request, 'post/post.html', context)

    @method_decorator(login_required(login_url='login'))
    @method_decorator(csrf_protect)
    def post(self, request, p):
        post = Post.objects.get(id=p)
        form = CommentForm(request.POST)
        comment = Comment.objects.create(
            owner=request.user,
            book=post.book,
            post=post,
            body=request.POST.get('body')
        )

        if comment is not None:
            return redirect('post', p=post.id)

        context = {'post': post, 'comment': comment, "form": form}
        return render(request, 'post/post.html', context)


class UpdatePostView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, p):
        post = Post.objects.get(id=p)
        form = PostForm(instance=post)
        books = Book.objects.all()

        context = {'form': form, 'books': books, 'post': post}
        return render(request, 'post/post_form.html', context)

    @method_decorator(login_required(login_url='login'))
    @method_decorator(csrf_protect)
    def post(self, request, p):
        post = Post.objects.get(id=p)
        form = PostForm(instance=post)
        books = Book.objects.all()
        if self.request.user != post.owner:
            return HttpResponse('You cannot make changes. You are not the owner of the post.')

        book_name = request.POST.get('book')
        book, created = Book.objects.get_or_create(name=book_name)

        post.book = book,
        post.name = request.POST.get('name'),
        post.body = request.POST.get('body'),
        post.save()

        if post is not None:
            return redirect('home')

        context = {'form': form, 'books': books, 'post': post}
        return render(request, 'post/post_form.html', context)


class DeletePostView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, p):
        post = Post.objects.get(id=p)

        return render(request, 'post/delete_post.html', {'obj': post})

    @method_decorator(login_required(login_url='login'))
    @method_decorator(csrf_protect)
    def post(self, request, p):
        post = Post.objects.get(id=p)

        if post is not None:
            post.delete()
            return redirect('home')

        return render(request, 'post/delete_post.html', {'obj': post})

