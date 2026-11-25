from django.db import models
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.CharField(max_length = 255)
    createdAt = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True,upload_to="images/")

class Like(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    # related_name value is used to reference the linked object from other linked object
    # eg if related_name = likesTEST -> we can use post.likesTEST
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["author", "post"],
                name="unique_author_like_post"
            ),
        ]


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.CharField(max_length = 255)
    createdAt = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
