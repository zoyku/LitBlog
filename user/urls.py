from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('login/', views.UserLoginView.as_view(), name="login"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('logout/', views.UserLogoutView.as_view(), name="logout"),
    path('profile/<str:user_id>/', views.UserProfileView.as_view(), name="profile"),
    path('edit-profile/<str:user_id>/', views.UserProfileEditView.as_view(), name="edit-profile"),
    path('edit-security/<str:user_id>/', views.UserSecurityEditView.as_view(), name="edit-security"),
]
