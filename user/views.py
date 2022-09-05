from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Book, Users
from post.models import Post
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .forms import UserRegisterForm
from post.forms import PostForm
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

