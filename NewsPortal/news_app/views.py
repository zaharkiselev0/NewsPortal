from copy import deepcopy

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Post, Puser
from .forms import PostForm
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            puser = self.request.user.puser
            sub_pk = context['post'].puser.pk
            subscribed = puser.subscriptions.filter(pk=sub_pk).exists()
            context['subscribed'] = subscribed
            context['sub_pk'] = sub_pk
        return context


class NewCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_edit.html'
    form_class = PostForm

    def form_valid(self, form):
        new = form.save(commit=False)
        new.article = False
        new.puser = self.request.user.puser
        return super().form_valid(form)


class ArticleCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_edit.html'
    form_class = PostForm

    def form_valid(self, form):
        new = form.save(commit=False)
        new.article = True
        new.puser = self.request.user.puser
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news_app.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news_app.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


def get_view(view_class, decorators):
    view = type('', view_class.__bases__, deepcopy(dict(view_class.__dict__)))
    for foo, args in decorators.items():
        foo(view, *args)
    return view



