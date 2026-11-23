from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('feed/', views.posts,name='feed'),
    path("login/", LoginView.as_view(redirect_authenticated_user=True,template_name="loginTemplate.html"), name="login"),
    # redirect_authenticated_user=True skips the login form when someone that has logged in opens /login
]