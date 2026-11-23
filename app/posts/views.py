from django.shortcuts import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from .models import Post

# Create your views here.
# @login_required
@login_required(login_url="login")
def posts(request):
    allPosts = Post.objects.order_by("-createdAt")
    template = loader.get_template('initialTemplate.html')
    context = {'allPost':allPosts}
    return HttpResponse(template.render(context,request))
