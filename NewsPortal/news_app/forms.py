from django import forms
from .models import Post
from django_filters import ModelChoiceFilter
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'category']
        labels = {'title': 'Заголовок', 'text': 'Текст', 'author': 'Автор(временно)', 'category': "Категория"}

