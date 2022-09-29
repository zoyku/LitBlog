
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from room.models import Room
from .models import Users, Book, Author
from post.models import Post
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .forms import UserRegisterForm, UserEditForm, UserSecurityForm, BookRegisterForm
from django.utils.decorators import method_decorator
from user.kmeans import kmeans
# import matplotlib.pyplot as plt

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

        rooms = Room.objects.filter(Q(book__name__icontains=param) |
                                    Q(name__icontains=param))

        books = Book.objects.annotate(post_count=Count('post_book', distinct=True),
                                      room_count=Count('room_book', distinct=True)).filter(name__icontains=param)

        item_count = posts.count() + rooms.count()

        post_paginator = Paginator(posts, 5)
        book_paginator = Paginator(books, 10)
        room_paginator = Paginator(rooms, 7)
        post_page = request.GET.get('post_page')
        book_page = request.GET.get('book_page')
        room_page = request.GET.get('room_page')
        if post_page is not None:
            post_page = post_page
        else:
            post_page = 1
        if book_page is not None:
            book_page = book_page
        else:
            book_page = 1
        if room_page is not None:
            room_page = room_page
        else:
            room_page = 1
        post_page_obj = post_paginator.get_page(post_page)
        book_page_obj = book_paginator.get_page(book_page)
        room_page_obj = room_paginator.get_page(room_page)
        context = {'post_page_obj': post_page_obj, 'book_page_obj': book_page_obj,
                   'room_page_obj': room_page_obj, 'posts': posts, 'item_count': item_count}
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


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        request.user.online = 0
        request.user.save()
        logout(request)
        return redirect('home')


class UserProfileView(View):
    def get(self, request, user_id):
        user = get_object_or_404(Users, id=user_id)
        posts = user.post_owner.all()
        books = Book.objects.annotate(post_count=Count('post_book', filter=Q(post_book__owner=user),
                                                       distinct=True), room_count=Count('room_book',
                                                                                        filter=(
                                                                                                    Q(room_book__owner=user) |
                                                                                                    Q(room_book__participants=user)),
                                                                                        distinct=True)).filter(
                                                                                                                Q(post_book__owner=user) |
                                                                                                                Q(room_book__owner=user) |
                                                                                                                Q(room_book__participants=user))

        all_rooms = Room.objects.annotate(participant_count=Count('participants', distinct=True),
                                          chat_count=Count('chat_room', distinct=True))

        rooms = Room.objects.filter(Q(owner=user) | Q(participants=user)).distinct()

        all_labeled_data, user_labeled_data = kmeans(all_rooms, rooms)

        zeroth = user_labeled_data.count(0)
        first = user_labeled_data.count(1)

        print(first)
        print(zeroth)
        print(all_labeled_data)

        if first >= zeroth:
            for i in range(len(all_labeled_data)):
                if all_labeled_data[i][2] == 0:
                    all_rooms = all_rooms.exclude(name=all_rooms[i].name)
                    i -= 1
                    print(all_rooms)
        else:
            for i in range(len(all_labeled_data)):
                if all_labeled_data[i][2] == 1:
                    all_rooms = all_rooms.exclude(name=all_rooms[i].name)
                    i -= 1
                    print(all_rooms)

        print(all_rooms)

        item_count = posts.__len__() + rooms.__len__()

        author_books = Book.objects.filter(author__user=user)

        post_paginator = Paginator(posts, 5)
        book_paginator = Paginator(books, 10)
        room_paginator = Paginator(rooms, 7)
        post_page = request.GET.get('post_page')
        book_page = request.GET.get('book_page')
        room_page = request.GET.get('room_page')
        if post_page is not None:
            post_page = post_page
        else:
            post_page = 1
        if book_page is not None:
            book_page = book_page
        else:
            book_page = 1
        if room_page is not None:
            room_page = room_page
        else:
            room_page = 1
        post_page_obj = post_paginator.get_page(post_page)
        book_page_obj = book_paginator.get_page(book_page)
        room_page_obj = room_paginator.get_page(room_page)
        context = {'post_page_obj': post_page_obj, 'book_page_obj': book_page_obj, 'room_page_obj': room_page_obj,
                   'posts': posts, 'user': user, 'item_count': item_count, 'author_books': author_books}
        return render(request, 'user/profile.html', context)


class UserProfileEditView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = Users.objects.get(id=user_id)
        form = UserEditForm(instance=user)

        return render(request, 'user/edit_user.html', {'form': form})

    @method_decorator(csrf_protect)
    def post(self, request, user_id):
        user = Users.objects.get(id=user_id)
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=user.id)

        return render(request, 'user/edit_user.html', {'form': form})


class UserSecurityEditView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(Users, id=user_id)
        form = UserSecurityForm(instance=user)

        return render(request, 'user/edit_user.html', {'form': form})

    @method_decorator(csrf_protect)
    def post(self, request, user_id):
        user = get_object_or_404(Users, id=user_id)
        form = UserSecurityForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=user.id)

        return render(request, 'user/edit_user.html', {'form': form})


class RegisterAsAuthor(LoginRequiredMixin, View):
    def get(self, request, user_id):
        form = BookRegisterForm()

        return render(request, 'user/book_form.html', {'form': form})

    @method_decorator(csrf_protect)
    def post(self, request, user_id):
        user = get_object_or_404(Users, id=user_id)
        form = BookRegisterForm()
        book_name = request.POST.get('name')
        book, created = Book.objects.get_or_create(defaults={'name': book_name}, name__iexact=book_name)
        author, created = Author.objects.get_or_create(user=user)
        author.save()
        user.is_author = True
        user.save()
        book.author = author
        book.save()
        return redirect('profile', user_id=user.id)
