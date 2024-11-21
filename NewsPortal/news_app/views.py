from copy import deepcopy

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy


class PostList(ListView):
    queryset = Post.objects.all()
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = '-date'
    extra_context = {'before': [], 'after': []}


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class NewCreate(CreateView):
    model = Post
    template_name = 'post_edit.html'
    form_class = PostForm

    def form_valid(self, form):
        new = form.save(commit=False)
        new.article = False
        return super().form_valid(form)


class ArticleCreate(CreateView):
    model = Post
    template_name = 'post_edit.html'
    form_class = PostForm

    def form_valid(self, form):
        new = form.save(commit=False)
        new.article = True
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


def get_view(view_class, decorators):
    view = type('', view_class.__bases__, deepcopy(dict(view_class.__dict__)))
    for foo, *args in decorators:
        foo(view, *args)
    return view




