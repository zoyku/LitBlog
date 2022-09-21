from django.urls import path
from . import views

urlpatterns = [
    path('create-post/', views.CreatePostView.as_view(), name="create-post"),
    path('update-post/<str:post_id>/', views.UpdatePostView.as_view(), name="update-post"),
    path('rate-post/', views.RatePostView.as_view(), name="rate-post"),
    path('detail/<str:post_id>/', views.PostView.as_view(), name="post"),
    path('delete-post/<str:post_id>/', views.DeletePostView.as_view(), name="delete-post"),
    path('delete-comment/<str:comment_id>/', views.DeleteCommentView.as_view(), name="delete-comment"),
    path('approve-post/', views.ApprovePostView.as_view(), name="approve-post"),
]
