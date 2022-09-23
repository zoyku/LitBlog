from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect

from room.models import Room
from user.models import Book
from .decorator import author_required
from .forms import PostForm, CommentForm
from .models import Post, Comment


class CreatePostView(LoginRequiredMixin, View):
    def get(self, request):
        form = PostForm()
        books = Book.objects.all()
        context = {"form": form, 'books': books}
        return render(request, 'post/post_form.html', context)

    @method_decorator(csrf_protect)
    def post(self, request):
        form = PostForm(request.POST)
        books = Book.objects.all()
        book_name = request.POST.get('book')
        book, created = Book.objects.get_or_create(defaults={'name': book_name}, name__iexact=book_name)

        post = Post.objects.create(
            owner=request.user,
            book=book,
            name=request.POST.get('name'),
            body=request.POST.get('body'),
        )

        if post is not None:
            return redirect('home')

        context = {"form": form, 'books': books}

        return render(request, 'post/post_form.html', context)


class PostView(View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        comments = post.comment_set.all()
        form = CommentForm(request.POST)
        author = post.book.author.user if post.book.author is not None else None

        user_id = request.user.id
        user_likes = post.likes.all()
        is_there = user_likes.filter(id=user_id).count()

        liked = 1 if is_there == 1 else 0

        context = {'post': post, 'comments': comments, "form": form, "liked": liked, 'author': author}
        return render(request, 'post/post.html', context)

    @method_decorator(login_required(login_url='login'))
    @method_decorator(csrf_protect)
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        form = CommentForm(request.POST)
        comment = Comment.objects.create(
            owner=request.user,
            book=post.book,
            post=post,
            body=request.POST.get('body')
        )
        user_id = request.user.id
        user_likes = post.likes.all()
        is_there = user_likes.filter(id=user_id).count()

        liked = 1 if is_there == 1 else 0

        if comment is not None:
            return redirect('post', post_id=post.id)

        context = {'post': post, 'comment': comment, "form": form, "liked": liked}
        return render(request, 'post/post.html', context)


class UpdatePostView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        form = PostForm(instance=post)
        books = Book.objects.all()

        context = {'form': form, 'books': books, 'post': post}
        return render(request, 'post/post_form.html', context)

    @method_decorator(csrf_protect)
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        form = PostForm(instance=post)
        books = Book.objects.all()
        if self.request.user != post.owner:
            return HttpResponse('You cannot make changes. You are not the owner of the post.')

        book_name = request.POST.get('book', None)
        book, created = Book.objects.get_or_create(defaults={'name': book_name}, name__iexact=book_name)

        post.book = book
        post.name = request.POST.get('name')
        post.body = request.POST.get('body')
        post.save()

        if post is not None:
            return redirect('profile', user_id=post.owner_id)

        context = {'form': form, 'books': books, 'post': post}
        return render(request, 'post/post_form.html', context)


class DeletePostView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        return render(request, 'post/delete_post.html', {'obj': post})

    @method_decorator(csrf_protect)
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        post.delete()
        book_id = post.book_id
        book_count = Post.objects.filter(book_id=book_id).count() + Room.objects.filter(book_id=book_id).count()
        book = Book.objects.get(id=post.book_id)
        if book_count == 0 and book.author is None:
            book.delete()
        return redirect('profile', user_id=post.owner_id)


class RatePostView(LoginRequiredMixin, View):
    @method_decorator(csrf_protect)
    def post(self, request):
        post_id = int(request.POST.get('post_id', None))

        post = Post.objects.get(id=post_id)
        is_liked = request.user.post_likes.filter(id=post_id).exists()
        if is_liked:
            post.rating = post.rating - 1
            post.likes.remove(request.user)
            post.save()
        elif not is_liked:
            post.rating = post.rating + 1
            post.likes.add(request.user)
            post.save()

        return JsonResponse({'rate': post.rating})


class DeleteCommentView(LoginRequiredMixin, View):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

        return render(request, 'post/delete_comment.html', {'obj': comment})

    @method_decorator(csrf_protect)
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        post_id = comment.post_id

        if comment is not None:
            comment.delete()
            return redirect('post', post_id=post_id)

        return render(request, 'post/delete_comment.html', {'obj': comment})


class ApprovePostView(LoginRequiredMixin, View):
    @method_decorator(author_required(login_url='login'))
    @method_decorator(csrf_protect)
    def post(self, request):
        post_id = int(request.POST.get('post_id', None))

        post = Post.objects.get(id=post_id)
        is_approved = post.is_approved

        if is_approved:
            post.is_approved = False
            post.save()
        elif not is_approved:
            post.is_approved = True
            post.save()

        return JsonResponse({'approved': post.is_approved})

