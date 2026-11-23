from django.shortcuts import HttpResponse, redirect, render
from django.template import loader
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

# @login_required
@login_required(login_url="login")
def feed(request):
    allPosts = Post.objects.order_by("-createdAt")
    template = loader.get_template('initialTemplate.html')
    context = {'allPosts':allPosts}
    return HttpResponse(template.render(context,request))

@login_required(login_url="login")
def create_post(request):
    if request.method == 'POST':
        # request.POST contains the submitted form fields like body
        form = PostForm(request.POST)
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