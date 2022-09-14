import logging

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Users
from post.models import Post, Book
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .forms import UserRegisterForm, UserEditForm, UserSecurityForm
from django.utils.decorators import method_decorator
import logging
import logging.handlers


# Create your views here.


class HomeView(View):
    def get(self, request):
        param = self.request.GET.get('param')

        logging.debug('burda')

        if param is not None:
            param = param
        else:
            param = ''

        posts = Post.objects.filter(Q(book__name__icontains=param) |
                                    Q(name__icontains=param))
        post_paginator = Paginator(posts, 5)
        books = Book.objects.all()
        book_paginator = Paginator(books, 10)
        users = Users.objects.all()
        user_paginator = Paginator(users, 7)
        post_page = request.GET.get('post_page')
        book_page = request.GET.get('book_page')
        user_page = request.GET.get('user_page')
        if post_page is not None:
            post_page = post_page
        else:
            post_page = 1
        if book_page is not None:
            book_page = book_page
        else:
            book_page = 1
        if user_page is not None:
            user_page = user_page
        else:
            user_page = 1
        post_page_obj = post_paginator.get_page(post_page)
        book_page_obj = book_paginator.get_page(book_page)
        user_page_obj = user_paginator.get_page(user_page)
        context = {'post_page_obj': post_page_obj, 'book_page_obj': book_page_obj,
                   'user_page_obj': user_page_obj, 'posts': posts}
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
    def get(self, request, user_id):
        user = get_object_or_404(Users, id=user_id)
        users = Users.objects.all()
        posts = user.post_owner.all()
        books = Book.objects.filter(post_book__owner=user)

        post_paginator = Paginator(posts, 5)
        book_paginator = Paginator(books, 10)
        user_paginator = Paginator(users, 7)
        post_page = request.GET.get('post_page')
        book_page = request.GET.get('book_page')
        user_page = request.GET.get('user_page')
        if post_page is not None:
            post_page = post_page
        else:
            post_page = 1
        if book_page is not None:
            book_page = book_page
        else:
            book_page = 1
        if user_page is not None:
            user_page = user_page
        else:
            user_page = 1
        post_page_obj = post_paginator.get_page(post_page)
        book_page_obj = book_paginator.get_page(book_page)
        user_page_obj = user_paginator.get_page(user_page)
        context = {'post_page_obj': post_page_obj, 'book_page_obj': book_page_obj, 'user_page_obj': user_page_obj,
                   'posts': posts, 'user': user}
        return render(request, 'user/profile.html', context)


class UserProfileEditView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, user_id):
        user = Users.objects.get(id=user_id)
        form = UserEditForm(instance=user)

        return render(request, 'user/edit_user.html', {'form': form})

    @method_decorator(login_required(login_url='login'))
    @method_decorator(csrf_protect)
    def post(self, request, user_id):
        user = Users.objects.get(id=user_id)
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=user.id)

        return render(request, 'user/edit_user.html', {'form': form})


class UserSecurityEditView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, user_id):
        user = Users.objects.get(id=user_id)
        form = UserSecurityForm(instance=user)

        return render(request, 'user/edit_user.html', {'form': form})

    @method_decorator(login_required(login_url='login'))
    @method_decorator(csrf_protect)
    def post(self, request, user_id):
        user = Users.objects.get(id=user_id)
        form = UserSecurityForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=user.id)

        return render(request, 'user/edit_user.html', {'form': form})
