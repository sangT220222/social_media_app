from django.shortcuts import HttpResponse, redirect, render, get_object_or_404
from django.template import loader
from django.contrib.auth.decorators import login_required
from .models import Post, Like
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

def like_post(request, post_id):
    # checks if the primary key in Post object exists in the db
    post_object = get_object_or_404(Post, pk=post_id)
    # check if user has liked the post already
    already_liked = Like.objects.filter(author=request.user, post=post_object).exists()
    print(already_liked)
    if(already_liked == False):
        # post is a foreign key relating to Post object, hence we can assing it directly
        createLike = Like(author = request.user, post = post_object)
        createLike.save()
    
    return redirect("feed")