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
from .forms import UserRegisterForm, UserEditForm
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
                user.online = 1
                user.save()
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
            user.online = 1
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

        return render(request, 'user/register.html', {"form": form})


class UserLogoutView(View):
    def get(self, request):
        request.user.online = 0
        request.user.save()
        logout(request)
        return redirect('home')


class UserProfileView(View):
    def get(self, request, p):
        user = Users.objects.get(id=p)
        users = Users.objects.all()
        posts = user.post_set.all()
        books = Book.objects.all()

        context = {'user': user, 'posts': posts, 'books': books, 'users': users}
        return render(request, 'user/profile.html', context)


class UserProfileEditView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, p):
        user = Users.objects.get(id=p)
        form = UserEditForm(instance=user)

        return render(request, 'user/edit_user.html', {'form': form})

    @method_decorator(login_required(login_url='login'))
    @method_decorator(csrf_protect)
    def post(self, request, p):
        user = Users.objects.get(id=p)
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', p=user.id)

        return render(request, 'user/edit_user.html', {'form': form})
