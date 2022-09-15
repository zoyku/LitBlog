from django.urls import path
from . import views

urlpatterns = [
    path('detail/<str:room_id>/', views.RoomView.as_view(), name="room"),
    path('create-room/', views.CreateRoomView.as_view(), name="create-room"),
    path('update-room/<str:room_id>/', views.UpdateRoomView.as_view(), name="update-room"),
    path('delete-room/<str:room_id>/', views.DeleteRoomView.as_view(), name="delete-room")
]
