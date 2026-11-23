from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    # specifies which model to use
    class Meta:
        model = Post
        # User enters the body, view sets author, django sets createdAt on first save
        fields=["body"]