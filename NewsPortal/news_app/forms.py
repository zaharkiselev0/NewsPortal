from django import forms
from .models import Post
from django_filters import ModelChoiceFilter
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'category']
        labels = {'title': 'Заголовок', 'text': 'Текст', 'category': "Категория"}

