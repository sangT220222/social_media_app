from django.shortcuts import HttpResponse
from django.template import loader

# Create your views here.
def posts(request):
    template = loader.get_template('initialTemplate.html')
    return HttpResponse(template.render())
