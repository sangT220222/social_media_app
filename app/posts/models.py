from django.db import models
from django.conf import settings

# Create your models here.
class Feed(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.CharField(max_length = 255)
    createdAt = models.DateTimeField(auto_now_add=True)