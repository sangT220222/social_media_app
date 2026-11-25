from django.shortcuts import HttpResponse, redirect, render, get_object_or_404
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Post, Like
from .forms import PostForm, CommentForm
from django.contrib.auth.forms import UserCreationForm
from invitations.utils import get_invitation_model
from django.http import Http404
from django.db import transaction


# @login_required
@login_required(login_url="login")
def feed(request):
    allPosts = Post.objects.order_by("-createdAt")
    template = loader.get_template('initialTemplate.html')
    context = {'allPosts':allPosts, "comment_form": CommentForm()}
    return HttpResponse(template.render(context,request))

@login_required(login_url="login")
def create_post(request):
    if request.method == 'POST':
        # request.POST contains the submitted form fields like body
        form = PostForm(request.POST,request.FILES) #request.FILEs for images
        if form.is_valid():
            # commit=False gives Post object in memeory with body filled in only, not author yet
            post = form.save(commit=False)
            post.author = request.user
            # writes complete data to SQLITE, view populates the author
            post.save()
            # redirect back to feed page when post is submitted
            return redirect("feed")
    else:
        form = PostForm()
    return render(request,"create_post.html", {"form":form})

@login_required(login_url="login")
@require_POST
def like_post(request, post_id):
    post_object = get_object_or_404(Post, pk=post_id)
    # reuse an existing like on repeat. The unique constrainst on
    # (author,post) prevents duplicates if requests arrive together
    # to prevent same like being written from parallel requests, get_or_create() helps avoid a conflic
    Like.objects.get_or_create(author = request.user, post = post_object)
    return redirect("feed")

@login_required(login_url="login")
@require_POST
def comment_post(request, post_id):
    post_object = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post_object
        comment.save()
        return redirect("feed")
    return render(request,"initialTemplate.html", {"allPosts": Post.objects.order_by("-createdAt"),"comment_form": CommentForm(), "submitted_form": form,"submitted_post_id": post_id,})

def register_user(request, invite_key):
    Invitation = get_invitation_model()
    invitation = Invitation.objects.filter(key=invite_key, accepted=False, sent__isnull=False).first()
    if invitation is None or invitation.key_expired():
        raise Http404("Invitation is invalid, expired or has been used")
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                updated = Invitation.objects.filter(pk=invitation.pk, accepted=False).update(accepted=True)
                if updated == 0 :
                    raise Http404("This invitation has already been used.")
        
                form.save()
            return redirect("feed")
    else:
        form = UserCreationForm()
    return render(request, "register_user.html", {"form":form})