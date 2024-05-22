from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    text = forms.CharField()

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'author',
            'category',
        ]

