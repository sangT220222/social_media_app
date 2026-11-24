from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

# route definition 
urlpatterns = [
    path('feed/', views.feed,name='feed'),
    path("login/", LoginView.as_view(redirect_authenticated_user=True,template_name="loginTemplate.html"), name="login"),
    # redirect_authenticated_user=True skips the login form when someone that has logged in opens /login
    path("posts/new/", views.create_post, name='create_post'),
    path("like_post/<int:post_id>/", views.like_post, name="like_post"),
    path("comment_post/<int:post_id>", views.comment_post, name = "comment_post"),
]