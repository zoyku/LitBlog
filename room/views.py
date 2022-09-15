from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect

from post.models import Book
from room.forms import RoomForm
from room.models import Room, Chat


class RoomView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        chats = room.chat_set.all()
        participants = room.participants.all()

        context = {'room': room, 'chats': chats, 'participants': participants}
        return render(request, 'room/room.html', context)

    @method_decorator(login_required(login_url='login'))
    @method_decorator(csrf_protect)
    def post(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        chats = room.chat_set.all()
        participants = room.participants.all()

        new_message = Chat.objects.create(
            owner=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)

        if new_message is not None:
            return redirect('room', room_id=room.id)

        context = {'room': room, 'chats': chats, 'participants': participants}
        return render(request, 'room/room.html', context)


class CreateRoomView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        form = RoomForm()
        books = Book.objects.all()

        context = {'form': form, 'books': books}
        return render(request, 'room/room_form.html', context)

    @method_decorator(login_required(login_url='login'))
    @method_decorator(csrf_protect)
    def post(self, request):
        form = RoomForm()
        books = Book.objects.all()
        book_name = request.POST.get('book')
        book, created = Book.objects.get_or_create(name=book_name)

        room = Room.objects.create(
            owner=request.user,
            book=book,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        room.participants.add(request.user)

        if room is not None:
            return redirect('room', room_id=room.id)

        context = {'form': form, 'books': books}
        return render(request, 'room/room_form.html', context)


class UpdateRoomView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        form = RoomForm(instance=room)
        books = Book.objects.all()

        context = {'form': form, 'books': books}
        return render(request, 'room/room_form.html', context)

    @method_decorator(login_required(login_url='login'))
    @method_decorator(csrf_protect)
    def post(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        form = RoomForm(instance=room)
        books = Book.objects.all()

        book_name = request.POST.get('book')
        book, created = Book.objects.get_or_create(name=book_name)
        room.name = request.POST.get('name')
        room.book = book
        room.description = request.POST.get('description')
        room.save()
        if room is not None:
            return redirect('profile', user_id=room.owner_id)

        context = {'form': form, 'books': books, 'room': room}
        return render(request, 'room/room_form.html', context)


class DeleteRoomView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)

        return render(request, 'room/delete_room.html', {'obj': room})

    @method_decorator(login_required(login_url='login'))
    @method_decorator(csrf_protect)
    def post(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)

        room.delete()
        book_id = room.book_id
        book_count = Room.objects.filter(book_id=book_id).count()
        if book_count == 0:
            book = Book.objects.get(id=room.book_id)
            book.delete()
        return redirect('profile', user_id=room.owner_id)

