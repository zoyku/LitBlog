from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Book, Post, Users
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .forms import UserRegisterForm, PostForm
from django.utils.decorators import method_decorator


# Create your views here.


class HomeView(View):
    def get(self, request):
        param = self.request.GET.get('param')

        if param is not None:
            param = param
        else:
            param = ''

        posts = Post.objects.filter(Q(book__name__icontains=param) |
                                     Q(name__icontains=param))
        books = Book.objects.all()
        users = Users.objects.all()
        context = {'posts': posts, 'books': books, 'users': users}
        return render(request, 'user/home.html', context)


class UserLoginView(View):
    def get(self, request):
        return render(request, 'user/login.html')

    @method_decorator(csrf_protect)
    def post(self, request):
        if request.method == 'POST':
            email = request.POST.get('email').lower()
            password = request.POST.get('password')
            try:
                user = Users.objects.get(email=email)
            except:
                messages.error(request, 'User does not exist')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Username OR password does not exit')

        context = {}
        return render(request, 'user/login.html', context)


class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'user/register.html', {"form": form})

    @method_decorator(csrf_protect)
    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

        return render(request, 'user/register.html', {"form": form})


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class CreatePostView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        form = PostForm()
        return render(request, 'user/post_form.html', {"form": form})

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

        return render(request, 'user/post_form.html', {"form": form})


class PostView(View):
    def get(self, request, p):
        post = Post.objects.get(id=p)
        return render(request, 'user/post.html', {'post': post})


class UpdatePostView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, p):
        post = Post.objects.get(id=p)
        form = PostForm(instance=post)
        books = Book.objects.all()

        context = {'form': form, 'books': books, 'post': post}
        return render(request, 'user/post_form.html', context)

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
        return render(request, 'user/post_form.html', context)


class DeletePostView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, p):
        post = Post.objects.get(id=p)

        return render(request, 'user/delete_post.html', {'obj': post})

    @method_decorator(login_required(login_url='login'))
    @method_decorator(csrf_protect)
    def post(self, request, p):
        post = Post.objects.get(id=p)

        if post is not None:
            post.delete()
            return redirect('home')

        return render(request, 'user/delete_post.html', {'obj': post})
