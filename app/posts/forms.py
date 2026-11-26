from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    # specifies which model to use
    class Meta:
        model = Post
        # User enters the body, view sets author, django sets createdAt on first save
        fields=["body","image"]
        labels={"body": "Post text (required)", "image": "Photo (optional)"}
        widgets ={
            "body": forms.Textarea(attrs={"rows": 4}),
        }
class CommentForm(forms.ModelForm):
    # specifies which model to use
    class Meta:
        model = Comment
        fields=["body"]
        labels ={"body": ""}