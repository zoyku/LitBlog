from django.urls import path
from . import views

urlpatterns = [
    path('create-post/', views.CreatePostView.as_view(), name="create-post"),
    path('update-post/<str:p>/', views.UpdatePostView.as_view(), name="update-post"),
    path('<str:p>/', views.PostView.as_view(), name="post"),
    path('delete-post/<str:p>/', views.DeletePostView.as_view(), name="delete-post"),
]
