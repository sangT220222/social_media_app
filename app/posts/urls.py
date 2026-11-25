from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static

# route definition 
urlpatterns = [
    path('feed/', views.feed,name='feed'),
    path("login/", LoginView.as_view(redirect_authenticated_user=True,template_name="loginTemplate.html"), name="login"),
    # redirect_authenticated_user=True skips the login form when someone that has logged in opens /login
    path("posts/new/", views.create_post, name='create_post'),
    path("like_post/<int:post_id>/", views.like_post, name="like_post"),
    path("comment_post/<int:post_id>", views.comment_post, name = "comment_post"),
    path("register/", views.register_user, name="register_user"),
]

# when request starts with /media/, take the rest of the path and look for it inside media folder
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)