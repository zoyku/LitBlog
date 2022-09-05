from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('login/', views.UserLoginView.as_view(), name="login"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('logout/', views.UserLogoutView.as_view(), name="logout"),
    path('create-post/', views.CreatePostView.as_view(), name="create-post"),
    path('update-post/<str:p>/', views.UpdatePostView.as_view(), name="update-post"),
    path('post/<str:p>/', views.PostView.as_view(), name="post"),
    path('delete-post/<str:p>/', views.DeletePostView.as_view(), name="delete-post"),

]
